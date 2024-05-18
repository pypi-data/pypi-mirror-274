#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File  : coco
@Author: Yingping Li
@Time  : 2022/12/8 8:47
@Desc  :
"""
import json as jsonlib
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import click
import cv2
import numpy as np
import pandas as pd
import sweetviz as sv
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold
from pycocotools.coco import COCO
from tabulate import tabulate

WD_PREFIX = Path(os.path.curdir)


@click.group("coco", help="Toolkits to better use datasets under COCO type")
@click.option("--prefix", help="Image prefix")
@click.option("--json", help="JSON file")
@click.pass_context
def cli(ctx, prefix, json):
    ctx.ensure_object(dict)
    ctx.obj["prefix"] = prefix
    ctx.obj["json"] = json


@cli.command("eda", help="Exploratory Data Analysis")
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
    prefix = ctx.obj["prefix"]
    json = ctx.obj["json"]

    id2name, full_dataset, titles = extract_infos(prefix, json, cv)

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
    click.echo("---------------------------------------------------")
    click.echo(f"Categories number: {len(id2name)}")
    click.echo(f"Categories name: {tuple(id2name.values())}")
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
@click.option("--prefix", help="Image prefix")
@click.option("--json", nargs=2, help="JSON file")
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
def compare(prefix, json, out_dir, cv, area_thres):
    train_json, val_json = json

    id2name, train_dataset, titles = extract_infos(prefix, train_json, cv)
    _, val_dataset, _ = extract_infos(prefix, val_json, cv)

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
    click.echo("---------------------------------------------------")
    click.echo(f"Categories number: {len(id2name)}")
    click.echo(f"Categories name: {tuple(id2name.values())}")
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
@click.pass_context
def kfold(ctx, k, out_dir):
    def _gen_coco_dict(id2name):
        now = datetime.now()
        data = dict(
            info=dict(
                description=None,
                url=None,
                version=None,
                year=now.year,
                contributor=None,
                date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ),
            licenses=[dict(url=None, id=0, name=None,)],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            type="instances",
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=[
                # supercategory, id, name
            ],
        )

        # Append categories
        for id_, name in id2name.items():
            data["categories"].append(dict(supercategory=None, id=id_, name=name,))

        return data

    json = ctx.obj["json"]
    click.secho(
        f"Split COCO datasets define by JSON file: {json} to K-fold", fg="yellow"
    )
    coco = COCO(json)

    id2name = {}
    for category in coco.dataset["categories"]:
        id2name[category["id"]] = category["name"]

    imgIds = coco.getImgIds()

    full_dataset = []
    with click.progressbar(imgIds) as bar:
        for imgId in bar:
            annIds = coco.getAnnIds(imgIds=imgId)
            anns = coco.loadAnns(annIds)
            cnt = Counter([id2name.get(ann["category_id"]) for ann in anns])
            full_dataset.append([imgId] + [cnt.get(k, 0) for k in id2name.values()])

    df = pd.DataFrame(full_dataset, columns=["id"] + list(id2name.values()))

    mskf = MultilabelStratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    df["fold"] = -1

    num_bins = int(np.floor(1 + np.log2(len(df))))
    click.echo(f"Cut each class number into {num_bins} bins")
    class_bins = [f"bin_{class_}" for class_ in id2name.values()]
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
        train_ids = df[df["fold"] != i]["id"].to_list()
        val_ids = df[df["fold"] == i]["id"].to_list()
        with (WD_PREFIX / out_dir / f"train_fold_{i}.json").open("w") as train:
            data = _gen_coco_dict(id2name)
            imgs = coco.loadImgs(train_ids)
            for img in imgs:
                data["images"].append(img)
                annIds = coco.getAnnIds(imgIds=img["id"])
                anns = coco.loadAnns(annIds)
                data["annotations"].extend(anns)
            jsonlib.dump(data, train)
        click.secho(
            f"Write {i}-th fold train set in json file: {str(WD_PREFIX / out_dir / f'train_fold_{i}.json')}",
            fg="green",
        )
        with (WD_PREFIX / out_dir / f"val_fold_{i}.json").open("w") as val:
            data = _gen_coco_dict(id2name)
            imgs = coco.loadImgs(val_ids)
            for img in imgs:
                data["images"].append(img)
                annIds = coco.getAnnIds(imgIds=img["id"])
                anns = coco.loadAnns(annIds)
                data["annotations"].extend(anns)
            jsonlib.dump(data, val)
        click.secho(
            f"Write {i}-th fold validation set in json file: {str(WD_PREFIX / out_dir / f'val_fold_{i}.json')}",
            fg="green",
        )


@cli.command("anchor", help="Generate anchors using K-means algorithm")
@click.option("--k", type=int, help="Number of anchors")
@click.pass_context
def anchor(ctx, k):
    pass


def extract_infos(
    prefix: str, json: str, cv: bool
) -> Tuple[Dict[int, str], List[List[Any]], List[str]]:
    click.secho(f"Load COCO datasets define by JSON file: {json}", fg="yellow")
    coco = COCO(json)

    id2name = {}
    for category in coco.dataset["categories"]:
        id2name[category["id"]] = category["name"]

    img_ids = coco.getImgIds()

    click.secho("Extract information from images and annotations", fg="yellow")
    full_dataset = []
    with click.progressbar(img_ids) as bar:
        for img_id in bar:
            img = coco.loadImgs(img_id)[0]
            filename = img["file_name"]
            annIds = coco.getAnnIds(
                imgIds=img["id"], catIds=id2name.keys(), iscrowd=None
            )
            anns = coco.loadAnns(annIds)
            gts = len(anns)
            img_info = [filename, gts]
            if cv:
                path = os.path.join(prefix, filename)
                image = cv2.imdecode(
                    np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED
                )
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                brightness = np.array(gray).mean()
                height, width = image.shape[0], image.shape[1]
                shape = f"{height}*{width}"
                img_info += [height, width, shape, brightness]

            for ann in anns:
                class_name = id2name.get(ann["category_id"])
                bbox = ann["bbox"]
                xmin = bbox[0]
                ymin = bbox[1]
                xmax = bbox[2] + bbox[0]
                ymax = bbox[3] + bbox[1]
                width = bbox[2]
                height = bbox[3]
                area = ann["area"]
                ratio = bbox[2] / (bbox[3] + 1e-6)
                full_dataset.append(
                    img_info
                    + [class_name, xmin, ymin, xmax, ymax, width, height, area, ratio]
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

    return id2name, full_dataset, titles


def eds_csv(
    df: pd.DataFrame,
    small_area_upper: Union[int, float] = 32.0 ** 2,
    medium_area_upper: Union[int, float] = 96.0 ** 2,
):
    table_header = [
        "Class Name",
        "Annotations",
        "Images",
        "X Min",
        "Y Min",
        "X Max",
        "Y Max",
        "Width",
        "Height",
        "Area",
        "Ratio",
        "Small Objs",
        "Medium Objs",
        "Large Objs",
    ]
    count_by_class = df.groupby("class").count()[["xmin"]]
    image_by_class = df.groupby("class").nunique()[["filename"]]
    mean_by_class = df.groupby("class").mean()[
        ["xmin", "ymin", "xmax", "ymax", "width", "height", "area", "ratio"]
    ]
    table_data = []
    for i in count_by_class.index:
        small = df[(df["class"] == i) & (df["area"] < small_area_upper)].count()["xmin"]
        medium = df[
            (df["class"] == i)
            & (df["area"].between(small_area_upper, medium_area_upper))
        ].count()["xmin"]
        large = df[(df["class"] == i) & (df["area"] > medium_area_upper)].count()[
            "xmin"
        ]
        table_data.append(
            [i]
            + count_by_class.loc[i].to_list()
            + image_by_class.loc[i].to_list()
            + mean_by_class.loc[i].to_list()
            + [small, medium, large]
        )
    click.echo(tabulate(table_data, headers=table_header, tablefmt="simple"))
