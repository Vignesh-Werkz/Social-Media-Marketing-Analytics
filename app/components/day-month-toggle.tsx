"use client";
import { Switch } from "@nextui-org/switch";
import { Tooltip } from "@nextui-org/tooltip";

import { DayIcon, MonthIcon } from "./icons";
import { Dispatch, SetStateAction } from "react";

export default function DayMonthToggle({
    isSelected,
    setIsSelected,
}: {
    isSelected: boolean;
    setIsSelected: Dispatch<SetStateAction<boolean>>;
}) {
    return (
        <span className="flex items-center space-x-4">
            <label>View By:</label>
            <Tooltip
                content={isSelected ? "30-Day View" : "6-Month View"}
                placement="bottom-start"
                offset={5}
            >
                <Switch
                    isSelected={isSelected}
                    onValueChange={setIsSelected}
                    color="default"
                    size="lg"
                    startContent={<DayIcon />}
                    endContent={<MonthIcon />}
                />
            </Tooltip>
        </span>
    );
}
