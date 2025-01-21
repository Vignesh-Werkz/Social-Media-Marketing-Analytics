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

import { useEffect, useState, useRef } from "react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";

import { Button } from "@nextui-org/button";
import { Breadcrumbs, BreadcrumbItem } from "@nextui-org/breadcrumbs";
import { Spacer } from "@nextui-org/spacer";
import { IndicatorData } from "@/components/indicator/types";

import CustomisedToaster from "@/components/toaster";
import DayMonthToggle from "@/components/day-month-toggle";

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function ViewIndicatorPage() {
    const router = useRouter();
    const hasFetched = useRef(false);

    const [indicatorsData, setIndicatorsData] = useState<Array<IndicatorData>>(
        []
    );
    const [isDay, setIsDay] = useState(true);

    const searchParams = useSearchParams();
    const indicatorList = JSON.parse(searchParams.get("indicators") as string);
    console.log(indicatorList);

    const datasets = indicatorsData.map((indicator) => ({
        label: indicator.indicatorName,
        data: isDay
            ? indicator.resultsByDay.map((result) => result.average_score)
            : indicator.resultsByMonth.map((result) => result.average_score),
        borderWidth: 3,
        pointStyle: "circle",
        tension: 0.3,
    }));
    const data = {
        labels: isDay
            ? indicatorsData[0]?.resultsByDay.map((results) => results.date)
            : indicatorsData[0]?.resultsByMonth.map((results) => results.date),
        datasets: datasets,
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

    const fetchIndicators = async () => {
        try {
            const indicatorQuery = indicatorList
                .map((indicator: string) => `name=${indicator}`)
                .join("&");
            const res = await fetch("/api/getindicators?" + indicatorQuery);
            const data = await res.json();
            const indiData = data as Array<IndicatorData>;
            console.log(indiData);
            const sortedIndiData = indiData.map((indicator) => ({
                ...indicator,
                resultsByDay: indicator.resultsByDay.sort(
                    (a, b) =>
                        new Date(a.date).getTime() - new Date(b.date).getTime()
                ),
                resultsByMonth: indicator.resultsByMonth.sort(
                    (a, b) =>
                        new Date(a.date).getTime() - new Date(b.date).getTime()
                ),
            }));
            setIndicatorsData(sortedIndiData);
        } catch (error) {
            console.error("Error fetching indicator: ", error);
        }
    };

    useEffect(() => {
        if (!hasFetched.current && indicatorList) {
            fetchIndicators();
            hasFetched.current = true;
        }
    }, [indicatorList]);

    return (
        <>
            <CustomisedToaster />

            <div className="inline-block w-full">
                <Breadcrumbs variant="solid" underline="hover">
                    <BreadcrumbItem onPress={() => router.push("/dashboard")}>
                        Dashboard
                    </BreadcrumbItem>
                    <BreadcrumbItem>Compare Indicators</BreadcrumbItem>
                </Breadcrumbs>
                <Spacer y={5} />
                <div className="flex justify-between items-center">
                    <h1 className={title()}>Compare Indicators</h1>
                    <div className="flex gap-4">
                        <Button onPress={() => router.push("/dashboard")}>
                            Back
                        </Button>
                    </div>
                </div>
                <Spacer y={3} />
                <div className="w-full flex items-center">
                    <span className="text-md mr-2">
                        Indicators: {indicatorList.join(", ")}
                    </span>
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
