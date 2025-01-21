"use client";
import { Card, CardBody, CardHeader } from "@nextui-org/card";
import { Divider } from "@nextui-org/divider";
import { Spacer } from "@nextui-org/spacer";
import { Slider } from "@nextui-org/slider";
import { Tooltip } from "@nextui-org/tooltip";

import { InfoIcon } from "../icons";

import { useState, useEffect } from "react";

import { ModelData } from "./types";

export const ModelBox = ({
    modelData,
    updateModelWeightsData,
}: {
    modelData: ModelData;
    updateModelWeightsData: (data: ModelData) => void;
}) => {
    const [modelDescription, setModelDescription] = useState<string>("");
    const handleSliderChange = (
        value: number | number[],
        key: keyof ModelData
    ) => {
        const newValue = Array.isArray(value) ? value[0] : value;
        const updatedModel = { ...modelData, [key]: newValue };
        updateModelWeightsData(updatedModel);
    };

    useEffect(() => {
        const fetchModelDescription = async () => {
            try {
                const res = await fetch(
                    "api/getmodeldescription?name=" + modelData.model_name
                );
                const desc = await res.json();
                setModelDescription(desc);
            } catch (error) {
                console.error("Error fetching model description:", error);
            }
        };
        fetchModelDescription();
    }, []);

    return (
        <Card
            className="min-w-[400px] max-w-[400px]"
            style={{ margin: "16px" }}
        >
            <CardHeader className="flex gap-3">
                <span className="text-lg">{modelData.model_name}</span>
                <Spacer x={5} />
                <Slider
                    label="Model Weight"
                    step={0.01}
                    maxValue={1}
                    minValue={0}
                    value={modelData.model_weight}
                    onChange={(value) =>
                        handleSliderChange(value, "model_weight")
                    }
                    renderLabel={({ children, ...props }) => (
                        <label
                            {...props}
                            className="text-medium flex gap-2 items-center"
                        >
                            {children}
                            <Tooltip
                                className="w-[200px] px-1.5 text-tiny text-default-600 rounded-small"
                                content="This is how much to prioritise this model"
                                placement="right"
                            >
                                <span className="transition-opacity opacity-80 hover:opacity-100">
                                    <InfoIcon />
                                </span>
                            </Tooltip>
                        </label>
                    )}
                />
            </CardHeader>
            <CardHeader className="flex gap-3">
                <span className="text-small">{modelDescription}</span>
            </CardHeader>
            <Divider />
            <CardBody>
                <Slider
                    label="Title Weight"
                    step={0.01}
                    maxValue={1}
                    minValue={0}
                    value={modelData.title_sentiment}
                    onChange={(value) =>
                        handleSliderChange(value, "title_sentiment")
                    }
                    renderLabel={({ children, ...props }) => (
                        <label
                            {...props}
                            className="text-medium flex gap-2 items-center"
                        >
                            {children}
                            <Tooltip
                                className="w-[200px] px-1.5 text-tiny text-default-600 rounded-small"
                                content="This is how much to prioritise the title of a post"
                                placement="right"
                            >
                                <span className="transition-opacity opacity-80 hover:opacity-100">
                                    <InfoIcon />
                                </span>
                            </Tooltip>
                        </label>
                    )}
                />
                <Spacer y={5} />
                <Slider
                    label="Selftext Weight"
                    step={0.01}
                    maxValue={1}
                    minValue={0}
                    value={modelData.selftext_sentiment}
                    onChange={(value) =>
                        handleSliderChange(value, "selftext_sentiment")
                    }
                    renderLabel={({ children, ...props }) => (
                        <label
                            {...props}
                            className="text-medium flex gap-2 items-center"
                        >
                            {children}
                            <Tooltip
                                className="w-[200px] px-1.5 text-tiny text-default-600 rounded-small"
                                content="This is how much to prioritise the content of a post"
                                placement="right"
                            >
                                <span className="transition-opacity opacity-80 hover:opacity-100">
                                    <InfoIcon />
                                </span>
                            </Tooltip>
                        </label>
                    )}
                />
                <Spacer y={5} />
                <Slider
                    label="Comment Weight"
                    step={0.01}
                    maxValue={1}
                    minValue={0}
                    value={modelData.comments_sentiment}
                    onChange={(value) =>
                        handleSliderChange(value, "comments_sentiment")
                    }
                    renderLabel={({ children, ...props }) => (
                        <label
                            {...props}
                            className="text-medium flex gap-2 items-center"
                        >
                            {children}
                            <Tooltip
                                className="w-[200px] px-1.5 text-tiny text-default-600 rounded-small"
                                content="This is how much to prioritise the comments of a post"
                                placement="right"
                            >
                                <span className="transition-opacity opacity-80 hover:opacity-100">
                                    <InfoIcon />
                                </span>
                            </Tooltip>
                        </label>
                    )}
                />
            </CardBody>
        </Card>
    );
};
