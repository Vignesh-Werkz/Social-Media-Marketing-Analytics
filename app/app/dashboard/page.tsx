"use client";
import { title } from "@/components/primitives";
import { Button } from "@nextui-org/button";
import { Input } from "@nextui-org/input";
import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    useDisclosure,
} from "@nextui-org/modal";
import { Select, SelectItem } from "@nextui-org/select";
import { SharedSelection } from "@nextui-org/system";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { IndicatorData } from "@/components/indicator/types";
import { AggregateData } from "@/components/aggregate-config/types";
import IndicatorSummary from "@/components/indicator/indicator-summary";
import DeleteConfirmationModal from "@/components/modals/delete-confirmation";
import CustomisedToaster from "@/components/toaster";
import DayMonthToggle from "@/components/day-month-toggle";

export default function DashboardPage() {
    const router = useRouter();

    const [indicatorsData, setIndicatorsData] = useState<Array<IndicatorData>>(
        []
    );
    const [aggregateList, setAggregateList] = useState<Array<AggregateData>>(
        []
    );
    const [newIndicatorName, setNewIndicatorName] = useState<string>("");
    const [newIndicatorAggregate, setNewIndicatorAggregate] =
        useState<SharedSelection>();
    const [newIndicatorFilters, setNewIndicatorFilters] = useState<string>("");
    const [selectedIndicatorName, setSelectedIndicatorName] =
        useState<string>("");

    const [isCompareMode, setIsCompareMode] = useState<boolean>(false);
    const [selectedIndicators, setSelectedIndicators] = useState<Array<string>>(
        []
    );
    const [isDay, setIsDay] = useState<boolean>(true);

    const {
        isOpen: isCreateOpen,
        onOpen: onCreateOpen,
        onOpenChange: onCreateOpenChange,
    } = useDisclosure();
    const {
        isOpen: isDeleteOpen,
        onOpen: onDeleteOpen,
        onOpenChange: onDeleteOpenChange,
    } = useDisclosure();

    const fetchIndicators = async () => {
        try {
            const res = await fetch("/api/getallindicators");
            const data = await res.json();
            const indiData = data as Array<IndicatorData>;
            setIndicatorsData(indiData);
        } catch (error) {
            console.error("Error fetching indicators: ", error);
        }
    };

    const clearData = () => {
        console.log(newIndicatorAggregate);
        setNewIndicatorName("");
        setNewIndicatorAggregate(undefined);
        setNewIndicatorFilters("");
    };

    const createNewIndicator = async () => {
        const newIndicatorData: IndicatorData = {
            indicatorName: newIndicatorName.trim(),
            filters: newIndicatorFilters
                .split(";")
                .map((filter) => filter.trim())
                .filter((filter) => filter.length > 0),
            aggregateName: newIndicatorAggregate?.currentKey || "",
            resultsByDay: [],
            resultsByMonth: [],
        };
        try {
            const response = await fetch("api/createindicator", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newIndicatorData),
            });

            if (response.ok) {
                const responseData = await response.json();
                toast.success("Successfully created indcator: " + responseData);
                fetchIndicators();
            } else {
                const errorData = await response.json();
                toast.error(
                    "Cannot create indicator: " + errorData.detail ||
                        "Unknown error occurred"
                );
            }
        } catch (error) {
            toast.error("Error creating indicator:" + error);
        }

        // Reset state
        clearData();
    };

    const deleteIndicator = async () => {
        try {
            const response = await fetch(
                `api/deleteindicator/?name=${selectedIndicatorName}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            if (response.ok) {
                const responseData = await response.json();
                toast.success("Successfully deleted indcator: " + responseData);
                setSelectedIndicatorName("");
                fetchIndicators();
            } else {
                const errorData = await response.json();
                toast.error(
                    "Cannot delete indicator: " + errorData.detail ||
                        "Unknown error occurred"
                );
            }
        } catch (error) {
            toast.error("Error deleting aggregate: " + error);
        }
    };

    const onDeleteClicked = (indicatorName: string) => {
        setSelectedIndicatorName(indicatorName);
        onDeleteOpen();
    };

    const onDuplicateClicked = (indicatorName: string) => {
        const duplicatingIndicator: IndicatorData = indicatorsData.find(
            (indicator) => indicator.indicatorName === indicatorName
        )!;

        if (duplicatingIndicator) {
            setNewIndicatorName(duplicatingIndicator.indicatorName + " Copy");
            setNewIndicatorAggregate(undefined);
            setNewIndicatorFilters(duplicatingIndicator.filters.join(";"));
            onCreateOpen();
        } else {
            console.error(`Indicator with name ${indicatorName} not found.`);
        }
    };

    const newIndicatorNameIsEmpty = newIndicatorName.trim() === "";
    const indicatorNameCheck = (name: string) =>
        indicatorsData.some(
            (indicator: IndicatorData) =>
                indicator.indicatorName === name.trim()
        );
    const newIndicatorNameExists = indicatorNameCheck(newIndicatorName);

    const isNewIndicatorInvalid = useMemo(
        () =>
            newIndicatorNameIsEmpty ||
            !newIndicatorAggregate ||
            newIndicatorNameExists,
        [newIndicatorName, newIndicatorAggregate]
    );

    useEffect(() => {
        fetchIndicators();
    }, []);

    useEffect(() => {
        const fetchAggregateList = async () => {
            try {
                const res = await fetch("/api/getallaggregates");
                const data = await res.json();
                const aggregates = data as Array<AggregateData>;
                setAggregateList(aggregates);
            } catch (error) {
                console.error("Error fetching indicators: ", error);
            }
        };
        fetchAggregateList();
    }, []);

    return (
        <>
            <CustomisedToaster />
            <Modal
                isOpen={isCreateOpen}
                onOpenChange={onCreateOpenChange}
                placement="top"
            >
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">
                                Create New Indicator
                            </ModalHeader>
                            <ModalBody>
                                <Input
                                    autoFocus
                                    isRequired
                                    label="Indicator Name"
                                    variant="bordered"
                                    value={newIndicatorName}
                                    onValueChange={setNewIndicatorName}
                                    isInvalid={
                                        newIndicatorNameIsEmpty ||
                                        newIndicatorNameExists
                                    }
                                    errorMessage={
                                        newIndicatorNameIsEmpty
                                            ? "Indicator name cannot be blank"
                                            : "This indicator name is already used"
                                    }
                                />
                                <Select
                                    isRequired
                                    label="Aggregate"
                                    placeholder="Select an aggregate"
                                    variant="bordered"
                                    selectionMode="single"
                                    selectedKeys={newIndicatorAggregate}
                                    onSelectionChange={setNewIndicatorAggregate}
                                    isInvalid={!newIndicatorAggregate}
                                    errorMessage="You have to select an aggregate"
                                >
                                    {aggregateList.map(
                                        (elem: AggregateData, id: number) => (
                                            <SelectItem
                                                key={elem.aggregateName}
                                                textValue={elem.aggregateName}
                                            >
                                                <div className="flex flex-col">
                                                    <span className="text-small">
                                                        {elem.aggregateName}
                                                    </span>
                                                    <span className="text-tiny text-default-400">
                                                        {elem.description}
                                                    </span>
                                                </div>
                                            </SelectItem>
                                        )
                                    )}
                                </Select>
                                <Input
                                    label="Filters"
                                    description="Type your filters separated by semi-colons ;"
                                    variant="bordered"
                                    value={newIndicatorFilters}
                                    onValueChange={setNewIndicatorFilters}
                                />
                            </ModalBody>
                            <ModalFooter>
                                <div className="flex w-full justify-between">
                                    <Button variant="light" onPress={clearData}>
                                        Clear
                                    </Button>
                                    <div className="flex gap-2">
                                        <Button
                                            variant="flat"
                                            onPress={onClose}
                                        >
                                            Close
                                        </Button>
                                        <Button
                                            color="primary"
                                            onPress={async () => {
                                                await createNewIndicator();
                                                onClose();
                                            }}
                                            isDisabled={isNewIndicatorInvalid}
                                        >
                                            Create
                                        </Button>
                                    </div>
                                </div>
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal>

            <DeleteConfirmationModal
                isDeleteOpen={isDeleteOpen}
                onDeleteOpenChange={onDeleteOpenChange}
                selectedItemName={selectedIndicatorName}
                onDeleteClicked={deleteIndicator}
                deleteType="Indicator"
            />

            <div className="inline-block w-full">
                <div className="flex justify-between items-center">
                    <h1 className={title()}>
                        {isCompareMode ? "Compare Indicators" : "Dashboard"}
                    </h1>
                    <div className="flex gap-4">
                        {isCompareMode && (
                            <Button
                                color="primary"
                                isDisabled={selectedIndicators.length < 2}
                                onClick={() =>
                                    router.push(
                                        "/compareindicators?indicators=" +
                                            JSON.stringify(selectedIndicators)
                                    )
                                }
                            >
                                Compare
                            </Button>
                        )}
                        <Button
                            onClick={() => {
                                setIsCompareMode(!isCompareMode);
                                if (isCompareMode) {
                                    setSelectedIndicators([]);
                                }
                            }}
                            color={isCompareMode ? "danger" : "default"}
                        >
                            {isCompareMode ? "Cancel" : "Compare Indicators"}
                        </Button>
                        {!isCompareMode && (
                            <Button
                                onPress={() => {
                                    clearData();
                                    onCreateOpen();
                                }}
                            >
                                Create New Indicator
                            </Button>
                        )}
                    </div>
                </div>
                <div className="flex mt-4 items-center">
                    <DayMonthToggle
                        isSelected={isDay}
                        setIsSelected={setIsDay}
                    />
                </div>
            </div>
            <div className="inline-block w-full text-center justify-center">
                <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10 w-full">
                    <div className="flex flex-wrap">
                        {indicatorsData &&
                            indicatorsData.map(
                                (indicator: IndicatorData, id: number) => (
                                    <IndicatorSummary
                                        key={id}
                                        indicatorData={indicator}
                                        onDeleteClicked={onDeleteClicked}
                                        onDuplicateClicked={onDuplicateClicked}
                                        refreshData={fetchIndicators}
                                        isCompareMode={isCompareMode}
                                        setSelectedIndicators={
                                            setSelectedIndicators
                                        }
                                        isDay={isDay}
                                    />
                                )
                            )}
                    </div>
                </section>
            </div>
        </>
    );
}
