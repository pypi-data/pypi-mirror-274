#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import shutil
from collections import Counter
from pathlib import Path
from typing import Any, List, Tuple

import click
import cv2
import numpy as np
import pandas as pd
import sweetviz as sv
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold

from lml.commands.coco import eds_csv
from lml.image.opencv import cv2Imread

WD_PREFIX = Path(os.path.curdir)


@click.group("yolo", help="Toolkits to better use datasets under Ultralytics COCO type")
@click.option("--image", help="Image prefix")
@click.option("--annotation", help="Annotation prefix")
@click.pass_context
def cli(ctx, image, annotation):
    ctx.ensure_object(dict)
    ctx.obj["image"] = image
    ctx.obj["annotation"] = annotation


@cli.command("eda")
@click.option("--out-dir", default="", help="Path to store analyze report")
@click.option(
    "--cv",
    is_flag=True,
    help="Use OpenCV to analyse raw image, which will save a lot of time",
)
@click.option(
    "--area-thres",
    nargs=2,
    type=float,
    default=(32.0 ** 2, 96.0 ** 2),
    help="Area threshold among small/medium/large objects",
)
@click.pass_context
def eda(ctx, out_dir, cv, area_thres):
    image_prefix = ctx.obj["image"]
    annotation_prefix = ctx.obj["annotation"]

    full_dataset, titles = extract_infos(image_prefix, annotation_prefix, cv)

    click.secho("Start EDA", fg="yellow")
    df = pd.DataFrame(full_dataset, columns=titles)
    images_df = df.drop_duplicates(subset=titles[0:-9])[titles[0:-9]]
    annotations_df = df[
        [
            "filename",
            "class",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "width",
            "height",
            "area",
            "ratio",
        ]
    ]
    images_report = sv.analyze(images_df)
    images_report.show_html(
        filepath=str(WD_PREFIX / out_dir / "IMAGES_SWEETVIZ_REPORT.html"),
        open_browser=False,
        layout="widescreen",
        scale=None,
    )
    annotations_report = sv.analyze(annotations_df)
    annotations_report.show_html(
        filepath=str(WD_PREFIX / out_dir / "ANNOTATIONS_SWEETVIZ_REPORT.html"),
        open_browser=False,
        layout="widescreen",
        scale=None,
    )

    click.echo("\n")
    click.echo("Simple Summary")
    # click.echo("---------------------------------------------------")
    # click.echo(f"Categories number: {len(id2name)}")
    # click.echo(f"Categories name: {tuple(id2name.values())}")
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.echo("---------------------------------------------------")
    eds_csv(df, *area_thres)
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.echo("---------------------------------------------------")
    click.echo(
        f"More analyze about images in File: {str(WD_PREFIX / 'IMAGES_SWEETVIZ_REPORT.html')}"
    )
    click.echo(
        f"More analyze about annotations in File: {str(WD_PREFIX / 'ANNOTATIONS_SWEETVIZ_REPORT.html')}"
    )
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.secho("Finish EDA", fg="green")


@cli.command(
    "compare", help="Exploratory Data Analysis between train set and validation set"
)
@click.option("--image", nargs=2, help="Image prefix")
@click.option("--annotation", nargs=2, help="Annotation prefix")
@click.option("--out-dir", default="", help="Path to store analyze report")
@click.option(
    "--cv",
    is_flag=True,
    help="Use OpenCV to analyse raw image, which will save a lot of time",
)
@click.option(
    "--area-thres",
    nargs=2,
    type=float,
    default=(32.0 ** 2, 96.0 ** 2),
    help="Area threshold among small/medium/large objects",
)
@click.pass_context
def compare(ctx, image, annotation, out_dir, cv, area_thres):
    train_image, val_image = image
    train_annotation, val_annotation = annotation

    train_dataset, titles = extract_infos(train_image, train_annotation, cv)
    val_dataset, _ = extract_infos(val_image, val_annotation, cv)

    click.secho("Start EDA", fg="yellow")
    train_df = pd.DataFrame(train_dataset, columns=titles)
    train_images_df = train_df.drop_duplicates(subset=titles[0:-9])[titles[0:-9]]
    train_annotations_df = train_df[
        [
            "filename",
            "class",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "width",
            "height",
            "area",
            "ratio",
        ]
    ]
    val_df = pd.DataFrame(val_dataset, columns=titles)
    val_images_df = val_df.drop_duplicates(subset=titles[0:-9])[titles[0:-9]]
    val_annotations_df = val_df[
        [
            "filename",
            "class",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "width",
            "height",
            "area",
            "ratio",
        ]
    ]
    images_report = sv.compare(
        [train_images_df, "Train Set"], [val_images_df, "Test Set"]
    )
    images_report.show_html(
        filepath=str(WD_PREFIX / out_dir / "IMAGES_COMPARE_REPORT.html"),
        open_browser=False,
        layout="widescreen",
        scale=None,
    )
    annotations_report = sv.compare(
        [train_annotations_df, "Train Set"], [val_annotations_df, "Test Set"]
    )
    annotations_report.show_html(
        filepath=str(WD_PREFIX / out_dir / "ANNOTATIONS_COMPARE_REPORT.html"),
        open_browser=False,
        layout="widescreen",
        scale=None,
    )

    click.echo("\n")
    click.echo("Simple Summary")
    # click.echo("---------------------------------------------------")
    # click.echo(f"Categories number: {len(id2name)}")
    # click.echo(f"Categories name: {tuple(id2name.values())}")
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.echo("---------------------------------------------------")
    click.echo("Train Set\n")
    eds_csv(train_df, *area_thres)
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.echo("---------------------------------------------------")
    click.echo("Test Set\n")
    eds_csv(val_df, *area_thres)
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.echo("---------------------------------------------------")
    click.echo(
        f"More analyze about images in File: {str(WD_PREFIX / 'IMAGES_COMPARE_REPORT.html')}"
    )
    click.echo(
        f"More analyze about annotations in File: {str(WD_PREFIX / 'ANNOTATIONS_COMPARE_REPORT.html')}"
    )
    click.echo("---------------------------------------------------")
    click.echo("\n")
    click.secho("Finish EDA", fg="green")


@cli.command(
    "kfold", help="Generate K-fold dataset for cross-validation using MSKF algorithm"
)
@click.option("--k", type=int, help="Number of folds")
@click.option("--out-dir", default="", help="Path to store the output K-fold dataset")
@click.option("--classes", type=int, help="Number of classes")
@click.pass_context
def kfold(ctx, k, out_dir, classes):
    image_prefix = Path(ctx.obj["image"])
    annotation_prefix = Path(ctx.obj["annotation"])
    click.secho(f"Split YOLO datasets in folder {image_prefix} to K-fold", fg="yellow")

    full_dataset = []
    with click.progressbar(image_prefix.glob("*")) as pbar:
        for image in pbar:
            annotation = annotation_prefix / image.with_suffix(".txt").name
            cnt = (
                Counter([line.split()[0] for line in annotation.open("r").readlines()])
                if annotation.exists()
                else Counter([])
            )
            full_dataset.append(
                [image.name] + [cnt.get(str(k), 0) for k in range(classes)]
            )

    df = pd.DataFrame(full_dataset, columns=["id"] + [str(i) for i in range(classes)])

    mskf = MultilabelStratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    df["fold"] = -1

    num_bins = int(np.floor(1 + np.log2(len(df))))
    click.echo(f"Cut each class number into {num_bins} bins")
    class_bins = [f"bin_{class_}" for class_ in range(classes)]
    for class_bin in class_bins:
        df.loc[:, class_bin] = pd.cut(df[class_bin[4:]], bins=num_bins, labels=False)
    indicator = class_bins if len(class_bins) > 1 else class_bins * 2
    click.echo(f"Using MSKF algorithm to split datasets into {k} folds")
    for fold, (train_idx, val_idx) in enumerate(
        mskf.split(X=df, y=df[indicator].values)
    ):
        df.loc[val_idx, "fold"] = fold

    if not (WD_PREFIX / out_dir).exists():
        os.makedirs(WD_PREFIX / out_dir)
    click.echo(f"Create {str(WD_PREFIX / out_dir)} to store K-fold datasets")
    for i in range(k):
        (WD_PREFIX / out_dir / f"train_fold_{i}" / "images").mkdir(
            parents=True, exist_ok=True
        )
        (WD_PREFIX / out_dir / f"train_fold_{i}" / "labels").mkdir(
            parents=True, exist_ok=True
        )
        (WD_PREFIX / out_dir / f"val_fold_{i}" / "images").mkdir(
            parents=True, exist_ok=True
        )
        (WD_PREFIX / out_dir / f"val_fold_{i}" / "labels").mkdir(
            parents=True, exist_ok=True
        )

    for image in image_prefix.glob("*"):
        fold = df[df["id"] == image.name]["fold"].tolist()[0]
        for i in range(k):
            if i == fold:
                shutil.copy(
                    image, WD_PREFIX / out_dir / f"val_fold_{i}" / "images" / image.name
                )
                if (annotation_prefix / image.with_suffix(".txt").name).exists():
                    shutil.copy(
                        annotation_prefix / image.with_suffix(".txt").name,
                        WD_PREFIX
                        / out_dir
                        / f"val_fold_{i}"
                        / "labels"
                        / image.with_suffix(".txt").name,
                    )
            else:
                shutil.copy(
                    image,
                    WD_PREFIX / out_dir / f"train_fold_{i}" / "images" / image.name,
                )
                if (annotation_prefix / image.with_suffix(".txt").name).exists():
                    shutil.copy(
                        annotation_prefix / image.with_suffix(".txt").name,
                        WD_PREFIX
                        / out_dir
                        / f"train_fold_{i}"
                        / "labels"
                        / image.with_suffix(".txt").name,
                    )


def extract_infos(
    image_prefix: str, annotation_prefix: str, cv: bool
) -> Tuple[List[List[Any]], List[str]]:
    click.secho(
        f"Parse annotations in folder {annotation_prefix} and image in folder{image_prefix}",
        fg="yellow",
    )
    full_dataset = []
    with click.progressbar(Path(image_prefix).glob("*")) as pbar:
        for image in pbar:
            if image.suffix not in [".jpg", ".jpeg", ".png"]:
                continue
            filename = image.name
            annotation = Path(annotation_prefix) / image.with_suffix(".txt").name
            if not annotation.exists():
                gts = 0
            else:
                with annotation.open("r") as anno:
                    gts = len(anno.readlines())
            img_info = [filename, gts]
            if cv:
                img = cv2Imread(image)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                brightness = np.array(gray).mean()
                height, width = img.shape[0], img.shape[1]
                shape = f"{height}*{width}"
                img_info += [height, width, shape, brightness]
            if annotation.exists():
                with annotation.open("r") as anno:
                    for line in anno:
                        content = list(map(float, line.split()))
                        class_id = int(content[0])
                        xmin = content[1] - content[3] / 2
                        ymin = content[2] - content[4] / 2
                        xmax = content[1] + content[3] / 2
                        ymax = content[2] + content[4] / 2
                        width = content[3]
                        height = content[4]
                        area = content[3] * content[4]
                        ratio = width / (height + 1e-6)
                        full_dataset.append(
                            img_info
                            + [
                                str(class_id),
                                xmin,
                                ymin,
                                xmax,
                                ymax,
                                width,
                                height,
                                area,
                                ratio,
                            ]
                        )
    titles = [
        "filename",
        "gts",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
        "width",
        "height",
        "area",
        "ratio",
    ]
    if cv:
        titles = [
            "filename",
            "gts",
            "im_height",
            "im_width",
            "shape",
            "brightness",
        ] + titles[2:]
    return full_dataset, titles
