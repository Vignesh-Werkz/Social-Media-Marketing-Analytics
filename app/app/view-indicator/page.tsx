"use client";
import { title } from "@/components/primitives";
import Chart from "chart.js/auto";
import {
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";

import { Button } from "@nextui-org/button";
import { Breadcrumbs, BreadcrumbItem } from "@nextui-org/breadcrumbs";
import { Spacer } from "@nextui-org/spacer";
import { useDisclosure } from "@nextui-org/modal";
import { EditIcon } from "@/components/icons";
import { IndicatorData } from "@/components/indicator/types";

import DeleteConfirmationModal from "@/components/modals/delete-confirmation";
import IndicatorFilters from "@/components/indicator/indicator-filters";
import EditFiltersModal from "@/components/modals/edit-filters";
import CustomisedToaster from "@/components/toaster";
import DayMonthToggle from "@/components/day-month-toggle";

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function ViewIndicatorPage() {
    const router = useRouter();
    const emptyIndicator: IndicatorData = {
        indicatorName: "",
        filters: [],
        aggregateName: "",
        resultsByDay: [],
        resultsByMonth: [],
    };
    const [indicatorData, setIndicatorData] =
        useState<IndicatorData>(emptyIndicator);
    const [isDay, setIsDay] = useState(true);

    const {
        isOpen: isDeleteOpen,
        onOpen: onDeleteOpen,
        onOpenChange: onDeleteOpenChange,
    } = useDisclosure();
    const {
        isOpen: isEditFiltersOpen,
        onOpen: onEditFiltersOpen,
        onOpenChange: onEditFiltersOpenChange,
    } = useDisclosure();

    const searchParams = useSearchParams();
    const indicatorName = searchParams.get("name");

    const results = isDay
        ? (indicatorData?.resultsByDay ?? [])
        : (indicatorData?.resultsByMonth ?? []);
    const sortedResults = [...results].sort(
        (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );
    const labels = sortedResults.map((result) => result.date);
    const dataPoints = sortedResults.map((result) => result.average_score);

    const data = {
        labels: labels,
        datasets: [
            {
                label: indicatorData.aggregateName,
                data: dataPoints,
                backgroundColor: "#ff1cf7",
                borderColor: "#ff1cf7",
                borderWidth: 3,
                pointStyle: "circle",
                tension: 0.3,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: "top" as const,
            },
            title: {
                display: false,
            },
        },
    };

    const fetchIndicator = async () => {
        try {
            const res = await fetch("/api/getindicator?name=" + indicatorName);
            const data = await res.json();
            const indiData = data as IndicatorData;
            console.log(indiData);
            setIndicatorData(indiData);
        } catch (error) {
            console.error("Error fetching indicator: ", error);
        }
    };

    const deleteIndicator = async () => {
        try {
            const response = await fetch(
                `api/deleteindicator/?name=${indicatorData.indicatorName}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            if (response.ok) {
                console.log(
                    "Successfully deleted aggregate: ",
                    indicatorData.indicatorName
                );
                router.push("/dashboard");
            } else {
                alert("Failed to delete aggregate. Try again later.");
            }
        } catch (error) {
            console.log("Error deleting aggregate: ", error);
        }
    };

    useEffect(() => {
        if (indicatorName) {
            fetchIndicator();
        }
    }, [indicatorName]);

    return (
        <>
            <CustomisedToaster />
            <DeleteConfirmationModal
                isDeleteOpen={isDeleteOpen}
                onDeleteOpenChange={onDeleteOpenChange}
                selectedItemName={indicatorData.indicatorName}
                onDeleteClicked={deleteIndicator}
                deleteType="Indicator"
            />

            <EditFiltersModal
                indicatorName={indicatorData.indicatorName}
                isOpen={isEditFiltersOpen}
                onOpenChange={onEditFiltersOpenChange}
                refreshData={fetchIndicator}
            />

            <div className="inline-block w-full">
                <Breadcrumbs variant="solid" underline="hover">
                    <BreadcrumbItem onPress={() => router.push("/dashboard")}>
                        Dashboard
                    </BreadcrumbItem>
                    <BreadcrumbItem>View Indicator</BreadcrumbItem>
                </Breadcrumbs>
                <Spacer y={5} />
                <div className="flex justify-between items-center">
                    <h1 className={title()}>{indicatorData.indicatorName}</h1>
                    <div className="flex gap-4">
                        <Button onPress={() => router.push("/dashboard")}>
                            Back
                        </Button>
                        <Button color="danger" onPress={onDeleteOpen}>
                            Delete
                        </Button>
                    </div>
                </div>
                <Spacer y={3} />
                <div className="w-full flex items-center">
                    <span className="text-md mr-2">Filters: </span>
                    {indicatorData && (
                        <IndicatorFilters
                            indicatorFilters={indicatorData.filters}
                        />
                    )}
                    <Button
                        isIconOnly
                        variant="light"
                        onClick={onEditFiltersOpen}
                    >
                        <EditIcon />
                    </Button>
                </div>
                <div className="flex mt-4 items-center">
                    <DayMonthToggle
                        isSelected={isDay}
                        setIsSelected={setIsDay}
                    />
                </div>
            </div>
            <section className="flex flex-col gap-4 py-8 md:py-10"></section>
            <Line data={data} options={options} />
            <section className="flex flex-col gap-4 py-8 md:py-10"></section>
        </>
    );
}
