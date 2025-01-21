import Chart from "chart.js/auto";
import {
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import { useDisclosure } from "@nextui-org/modal";
import { Line } from "react-chartjs-2";
import { Card, CardBody, CardFooter, CardHeader } from "@nextui-org/card";
import { Divider } from "@nextui-org/divider";
import {
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownItem,
    DropdownSection,
} from "@nextui-org/dropdown";
import { Button } from "@nextui-org/button";
import { Checkbox } from "@nextui-org/checkbox";
import {
    CopyDocumentIcon,
    DeleteDocumentIcon,
    EditDocumentIcon,
    HamburgerMenuIcon,
    ViewDocumentIcon,
} from "../icons";
import { IndicatorData } from "./types";
import EditFiltersModal from "../modals/edit-filters";
import IndicatorFilters from "./indicator-filters";

import { Dispatch, SetStateAction } from "react";

// Register the necessary components
Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function IndicatorSummary({
    indicatorData,
    onDeleteClicked,
    onDuplicateClicked,
    refreshData,
    isCompareMode,
    setSelectedIndicators,
    isDay,
}: {
    indicatorData: IndicatorData;
    onDeleteClicked: (indicatorName: string) => void;
    onDuplicateClicked: (indicatorName: string) => void;
    refreshData: () => Promise<void>;
    isCompareMode: boolean;
    setSelectedIndicators: Dispatch<SetStateAction<string[]>>;
    isDay: boolean;
}) {
    const {
        isOpen: isEditFiltersOpen,
        onOpen: onEditFiltersOpen,
        onOpenChange: onEditFiltersOpenChange,
    } = useDisclosure();
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
                borderWidth: 1,
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

    return (
        <Card style={{ margin: "16px", padding: "10px" }}>
            <EditFiltersModal
                indicatorName={indicatorData.indicatorName}
                isOpen={isEditFiltersOpen}
                onOpenChange={onEditFiltersOpenChange}
                refreshData={refreshData}
            />
            <CardHeader className="justify-between">
                <div className="flex gap-5">
                    <span className="text-lg">
                        {indicatorData.indicatorName}
                    </span>
                </div>
                {isCompareMode ? (
                    <Checkbox
                        onChange={(e) => {
                            if (e.target.checked) {
                                setSelectedIndicators((prev) => [
                                    ...prev,
                                    indicatorData.indicatorName,
                                ]);
                            } else {
                                setSelectedIndicators((prev) =>
                                    prev.filter(
                                        (indicatorName) =>
                                            indicatorName !=
                                            indicatorData.indicatorName
                                    )
                                );
                            }
                        }}
                    />
                ) : (
                    <Dropdown placement="right-start">
                        <DropdownTrigger>
                            <Button variant="faded" isIconOnly>
                                <HamburgerMenuIcon />
                            </Button>
                        </DropdownTrigger>
                        <DropdownMenu aria-label="Static Actions">
                            <DropdownSection title="Actions" showDivider>
                                <DropdownItem
                                    key="view"
                                    startContent={
                                        <ViewDocumentIcon className="iconClasses" />
                                    }
                                    description="View this indicator"
                                    href={
                                        "/view-indicator?name=" +
                                        indicatorData.indicatorName
                                    }
                                >
                                    View
                                </DropdownItem>
                                <DropdownItem
                                    key="edit"
                                    startContent={
                                        <EditDocumentIcon className="iconClasses" />
                                    }
                                    description="Change the list of filters used"
                                    onClick={onEditFiltersOpen}
                                >
                                    Edit Filters
                                </DropdownItem>
                                <DropdownItem
                                    key="duplicate"
                                    startContent={
                                        <CopyDocumentIcon className="iconClasses" />
                                    }
                                    description="Make a copy of this indicator"
                                    onClick={() =>
                                        onDuplicateClicked(
                                            indicatorData.indicatorName
                                        )
                                    }
                                >
                                    Duplicate
                                </DropdownItem>
                            </DropdownSection>

                            <DropdownSection title="Danger Zone">
                                <DropdownItem
                                    key="delete"
                                    className="text-danger"
                                    color="danger"
                                    startContent={
                                        <DeleteDocumentIcon className="iconClasses" />
                                    }
                                    description="Delete this indicator"
                                    onClick={() =>
                                        onDeleteClicked(
                                            indicatorData.indicatorName
                                        )
                                    }
                                >
                                    Delete
                                </DropdownItem>
                            </DropdownSection>
                        </DropdownMenu>
                    </Dropdown>
                )}
            </CardHeader>
            <Divider />
            <CardBody style={{ overflowX: "hidden", maxWidth: "100%" }}>
                <Line data={data} options={options} />
            </CardBody>
            <Divider />
            <CardFooter>
                {indicatorData && (
                    <IndicatorFilters
                        indicatorFilters={indicatorData.filters}
                    />
                )}
            </CardFooter>
        </Card>
    );
}
