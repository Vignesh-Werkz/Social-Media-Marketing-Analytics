"use client";

import { useState, useEffect } from "react";
import { toast, Toaster } from "sonner";
import { IndicatorData } from "../indicator/types";

import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
} from "@nextui-org/modal";

export default function EditFiltersModal({
    indicatorName,
    isOpen,
    onOpenChange,
    refreshData,
}: {
    indicatorName: string;
    isOpen: boolean;
    onOpenChange: () => void;
    refreshData: () => Promise<void>;
}) {
    const [indicatorData, setIndicatorData] = useState<IndicatorData>({
        indicatorName: "",
        filters: [],
        aggregateName: "",
        results: [],
    });
    const [indicatorFilters, setIndicatorFilters] = useState<string>("");

    const updateIndicatorFilter = async () => {
        const updatedFilters = indicatorFilters
            .split(";")
            .map((filter) => filter.trim());
        const updatedIndicatorData: IndicatorData = {
            ...indicatorData,
            filters: updatedFilters,
        };
        try {
            const response = await fetch("api/createindicator", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updatedIndicatorData),
            });

            if (response.ok) {
                const responseData = await response.json();
                toast.success(
                    "Successfully edited filters for " + responseData
                );
            } else {
                const errorData = await response.json();
                toast.error(
                    "Cannot edit filters: " + errorData.detail ||
                        "Unknown error occurred"
                );
            }
        } catch (error) {
            toast.error("Error updating filters:" + error);
        }
    };

    useEffect(() => {
        if (indicatorName === "") return;
        const fetchIndicatorFilter = async () => {
            try {
                const res = await fetch(
                    "/api/getindicator?name=" + indicatorName
                );
                const data = await res.json();
                const indiData = data as IndicatorData;
                setIndicatorData(indiData);
                setIndicatorFilters(indiData.filters.join(";"));
            } catch (error) {
                console.error("Error fetching indicator: ", error);
            }
        };
        fetchIndicatorFilter();
    }, [indicatorName]);
    return (
        <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
            <ModalContent>
                {(onClose) => (
                    <>
                        <ModalHeader className="flex flex-col gap-1">
                            Edit Filters
                        </ModalHeader>
                        <ModalBody>
                            <span className="text-sm">
                                You are editing filters for {indicatorName}
                            </span>
                            <Input
                                autoFocus
                                isRequired
                                label="Indicator Filters"
                                variant="bordered"
                                type="text"
                                value={indicatorFilters}
                                onValueChange={setIndicatorFilters}
                                description="Type your filters separated by semi-colons ;"
                            />
                        </ModalBody>
                        <ModalFooter>
                            <Button variant="flat" onPress={onClose}>
                                Cancel
                            </Button>
                            <Button
                                color="primary"
                                onPress={async () => {
                                    await updateIndicatorFilter();
                                    refreshData();
                                    onClose();
                                }}
                            >
                                Update Filters
                            </Button>
                        </ModalFooter>
                    </>
                )}
            </ModalContent>
        </Modal>
    );
}
