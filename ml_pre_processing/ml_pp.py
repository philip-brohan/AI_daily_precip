#!/usr/bin/env python

# Pre-process image to fill in missing data
# This version uses ML Table Transformer library
#  https://huggingface.co/docs/transformers/en/model_doc/table-transformer
# Method based on "https://github.com/NielsRogge/Transformers-Tutorials/blob/"+
#                 "master/Table%20Transformer/"+
#                 "Inference_with_Table_Transformer_(TATR)_for_parsing_tables.ipynb"

import os
import glob
import torch
from torchvision import transforms
from transformers import AutoModelForObjectDetection, TableTransformerForObjectDetection
from PIL import Image, ImageDraw
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="Image number", type=int, required=False, default=3)
parser.add_argument("--gallery", help="Use RJM's gallery images", action="store_true")
parser.add_argument("--debug", help="Output intermediate images", action="store_true")

args = parser.parse_args()

opdir = "."
if args.gallery:
    opdir = "%s/gemini/gallery/ml_pre_processing/%04d" % (
        os.getenv("SCRATCH"),
        args.img,
    )
    if not os.path.exists(opdir):
        os.makedirs(opdir)

if args.gallery:
    image_files = sorted(glob.glob(os.path.join("../images/RJM_gallery", "*.jpg")))
    img = Image.open(image_files[args.img - 1]).convert("RGB")
else:
    img = Image.open(
        "../images/jpgs_300dpi/Devon_1941-1950_RainNos_1651-1689-%d.jpg" % args.img
    ).convert("RGB")

model = AutoModelForObjectDetection.from_pretrained(
    "microsoft/table-transformer-detection", revision="no_timm"
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


# Transfomation to resize image so that the longest side is 800 pixels
class MaxResize(object):
    def __init__(self, max_size=800):
        self.max_size = max_size

    def __call__(self, image):
        width, height = image.size
        current_max_size = max(width, height)
        scale = self.max_size / current_max_size
        resized_image = image.resize(
            (int(round(scale * width)), int(round(scale * height)))
        )

        return resized_image


# Define a custom transform to systematically increase contrast
class IncreaseContrast(object):
    def __init__(self, contrast_factor):
        self.contrast_factor = contrast_factor

    def __call__(self, img):
        return transforms.functional.adjust_contrast(img, self.contrast_factor)


# Before passing image to model:
# 1. Resize image so that the longest side is 800 pixels
# 2. Convert to tensor
# 3. Normalize the colour space
detection_transform = transforms.Compose(
    [
        MaxResize(800),
        transforms.ToTensor(),
        IncreaseContrast(contrast_factor=2),  # Systematically increase the contrast
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

# Convert image to tensor ready for the model
pixel_values = detection_transform(img).unsqueeze(0)
pixel_values = pixel_values.to(device)

# Run the image through the model
with torch.no_grad():
    outputs = model(pixel_values)


# Now we have the model output, but it's an instance of class
#  TableTransformerObjectDetectionOutput
# We need to turn it into information about tables in the image
#   Labels, and bounding boxes, and confidence scores.
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(-1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b


def outputs_to_objects(outputs, img_size):
    m = outputs.logits.softmax(-1).max(-1)
    pred_labels = list(m.indices.detach().cpu().numpy())[0]
    pred_scores = list(m.values.detach().cpu().numpy())[0]
    pred_bboxes = outputs["pred_boxes"].detach().cpu()[0]
    pred_bboxes = [elem.tolist() for elem in rescale_bboxes(pred_bboxes, img_size)]

    objects = []
    for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
        try:
            class_label = model.config.id2label[int(label)]
        except:
            class_label = "no object"
        if not class_label == "no object":
            objects.append(
                {
                    "label": class_label,
                    "score": float(score),
                    "bbox": [float(elem) for elem in bbox],
                }
            )

    return objects


detected_tables = outputs_to_objects(outputs, img.size)

# Now we have the objects, we can draw them on the image
if args.debug:
    imgd = img.copy()
    for table in detected_tables:
        draw = ImageDraw.Draw(imgd)
        draw.rectangle(table["bbox"], outline="red", width=10)

    imgd.save("%s/detected_tables.jpg" % opdir)

# We're only interested in images which have one big table

target_table = None
for table in detected_tables:
    if table["score"] < 0.5:  # Doesn't look very like a table
        continue
    bbox = table["bbox"]
    area_fraction = (
        (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) / (img.size[0] * img.size[1])
    )
    target_table = table
    break

if target_table is None:
    if args.debug:
        img.save("%s/detected_tables.jpg" % opdir)
        img.save("%s/table_structure.jpg" % opdir)
    raise ValueError("No suitable table found in image")

# Now we have the table, we can crop it out of the image
# Leave a bit of padding round the edges
t_bbox = target_table["bbox"]
padding = 10
t_bbox = [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding]
cropped_img = img.crop(t_bbox)

# Now we have the table image, we can pass it to the table structure model
# Same process as for table detection
structure_model = TableTransformerForObjectDetection.from_pretrained(
    "microsoft/table-structure-recognition-v1.1-all"
)
structure_model.to(device)


structure_transform = transforms.Compose(
    [
        MaxResize(1000),
        transforms.ToTensor(),
        IncreaseContrast(contrast_factor=2),  # Systematically increase the contrast
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

pixel_values = structure_transform(cropped_img).unsqueeze(0)
pixel_values = pixel_values.to(device)
# print(pixel_values.shape)

# Run the model
with torch.no_grad():
    outputs = structure_model(pixel_values)

# Extract results from tensou outputs
cells = outputs_to_objects(outputs, cropped_img.size)
# print(cells)

# Now we have the objects, we can draw them on the image
if args.debug:
    imgd = img.copy()
    for cell in cells:
        c_bbox = cell["bbox"]
        c_bbox[0] += t_bbox[0]
        c_bbox[1] += t_bbox[1]
        c_bbox[2] += t_bbox[0]
        c_bbox[3] += t_bbox[1]
        draw = ImageDraw.Draw(imgd)
        draw.rectangle(c_bbox, outline="red", width=10)

    imgd.save("%s/table_structure.jpg" % opdir)
