"use client";
import { AggregateConfig } from "@/components/aggregate-config/aggregateconfig";
import { AggregateData, ModelData } from "@/components/aggregate-config/types";
import { title } from "@/components/primitives";
import { Button } from "@nextui-org/button";
import { Input } from "@nextui-org/input";
import { Breadcrumbs, BreadcrumbItem } from "@nextui-org/breadcrumbs";
import { Spacer } from "@nextui-org/spacer";
import CustomisedToaster from "@/components/toaster";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

export default function EditAggregatePage() {
    const router = useRouter();

    const emptyAggData: AggregateData = {
        aggregateName: "",
        description: "",
        weights: [],
    };
    const searchParams = useSearchParams();
    const aggregateName = searchParams.get("name");
    const [aggregateData, setAggregateData] =
        useState<AggregateData>(emptyAggData);

    useEffect(() => {
        const fetchAggregate = async () => {
            try {
                const res = await fetch(
                    "api/getaggregate?name=" + aggregateName
                );
                const data = await res.json();
                const aggData = data as AggregateData;
                setAggregateData(aggData);
            } catch (error) {
                console.error("Error fetching aggregate:", error);
            }
        };

        fetchAggregate();
    }, []);

    const updateAggregateData = async () => {
        try {
            const response = await fetch("api/updateaggregate/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(aggregateData),
            });

            const data = await response.json();
            if (response.ok) {
                toast.success("Successfully updated aggregate");
            } else {
                const errorData = await response.json();

                toast.error(
                    "Cannot update aggregate: " + errorData.detail ||
                        "Unknown error occurred"
                );
            }
        } catch (error) {
            toast.error("Error updating aggregate: " + error);
        }
    };

    const updateModelWeightsData = (data: ModelData) => {
        setAggregateData((prevAggregate) => {
            const updateWeights = prevAggregate.weights.map((model) =>
                model.model_name === data.model_name ? data : model
            );
            return {
                ...prevAggregate,
                weights: updateWeights,
            };
        });
    };

    const updateAggregateDescription = (newDescription: string) => {
        setAggregateData((prevAggregate) => ({
            ...prevAggregate,
            description: newDescription,
        }));
    };

    return (
        <>
            <CustomisedToaster />
            <div className="inline-block w-full">
                <Breadcrumbs variant="solid" underline="hover">
                    <BreadcrumbItem onPress={() => router.push("/aggregates")}>
                        Aggregates
                    </BreadcrumbItem>
                    <BreadcrumbItem>Configuration</BreadcrumbItem>
                </Breadcrumbs>
                <Spacer y={5} />
                <div className="flex justify-between items-center">
                    <h1 className={title()}>
                        {aggregateData["aggregateName"]} Configuration
                    </h1>

                    <div className="flex gap-4">
                        <Button onPress={() => router.push("/aggregates")}>
                            Back
                        </Button>
                        <Button color="primary" onClick={updateAggregateData}>
                            Save Changes
                        </Button>
                    </div>
                </div>
            </div>
            <div className="inline-block max-w-lg text-center justify-center">
                <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
                    <Input
                        type="text"
                        label="Aggregate Description"
                        labelPlacement="outside"
                        value={aggregateData.description}
                        description="Give a short description of the characteristics of this aggregate."
                        onValueChange={(value) =>
                            updateAggregateDescription(value)
                        }
                    />
                </section>
                <section className="flex flex-col items-center justify-center gap-4">
                    <AggregateConfig
                        aggregateData={aggregateData}
                        updateModelWeightsData={updateModelWeightsData}
                    />
                </section>
            </div>
        </>
    );
}
