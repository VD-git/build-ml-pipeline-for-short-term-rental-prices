#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    # Cleaning the file downloaded
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv(args.output_artifact, index=False)
    logger.info(f"Dataframe was cleaned: {df.shape}")

    # Upload the artifact in W&B
    artifact = wandb.Artifact(name=args.output_artifact, type=args.output_type)
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    run.finish()
    logger.info(f"CSV File was created: {args.output_artifact}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the input artifact that will be downloaded",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact that will be uploaded in W&B",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of data of the artifact uploaded",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the uploaded artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int,
        help="Min price to be cut",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=int,
        help="Max price to be cut",
        required=True
    )

    args = parser.parse_args()

    go(args)
