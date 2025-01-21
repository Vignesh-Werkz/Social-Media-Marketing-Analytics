"use client";
import { AggregateData } from "@/components/aggregate-config/types";
import { EditIcon, DeleteIcon } from "@/components/icons";
import { title } from "@/components/primitives";
import { Button } from "@nextui-org/button";
import { Link } from "@nextui-org/link";
import { Spacer } from "@nextui-org/spacer";
import { Input } from "@nextui-org/input";
import {
    Table,
    TableBody,
    TableCell,
    TableColumn,
    TableHeader,
    TableRow,
} from "@nextui-org/table";
import { Tooltip } from "@nextui-org/tooltip";
import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    useDisclosure,
} from "@nextui-org/modal";

import { useEffect, useState, useMemo } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

import DeleteConfirmationModal from "@/components/modals/delete-confirmation";
import CustomisedToaster from "@/components/toaster";

export default function AggregatesPage() {
    const router = useRouter();
    const [aggregatesData, setAggregatesData] = useState<Array<AggregateData>>(
        []
    );
    const [selectedAggregateName, setSelectedAggregateName] =
        useState<string>("");
    const [newAggregateName, setNewAggregateName] = useState<string>("");

    const {
        isOpen: isDeleteOpen,
        onOpen: onDeleteOpen,
        onOpenChange: onDeleteOpenChange,
    } = useDisclosure();
    const {
        isOpen: isCreateOpen,
        onOpen: onCreateOpen,
        onOpenChange: onCreateOpenChange,
    } = useDisclosure();

    const fetchAggregates = async () => {
        try {
            const res = await fetch("/api/getallaggregates");
            const data = await res.json();
            setAggregatesData(data);
        } catch (error) {
            console.error("Error fetching aggregates: ", error);
        }
    };

    const deleteAggregate = async () => {
        try {
            const response = await fetch(
                `api/deleteaggregate/?name=${selectedAggregateName}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            if (response.ok) {
                const responseData = await response.json();
                toast.success(
                    "Successfully deleted aggregate: " + responseData
                );
                setSelectedAggregateName("");
                fetchAggregates();
            } else {
                const errorData = await response.json();
                toast.error(
                    "Cannot delete aggregate: " + errorData.detail ||
                        "Unknown error occurred"
                );
            }
        } catch (error) {
            toast.error("Error deleting aggregate: " + error);
        }
    };

    const createNewAggregate = async () => {
        try {
            const response = await fetch(
                `api/createaggregate/?name=${newAggregateName.trim()}`,
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (response.ok) {
                const responseData = await response.json();
                toast.success(
                    "Successfully created new aggregate: " + responseData
                );
                router.push("/edit-aggregate?name=" + newAggregateName.trim());
            } else {
                const errorData = await response.json();
                toast.error(
                    "Failed to create aggregate: " + errorData.detail ||
                        "Unknown error occurred"
                );
            }
            fetchAggregates();
        } catch (error) {
            console.log("Error creating aggregate: ", error);
        }
    };

    const aggNameExists = (name: string) =>
        aggregatesData.some(
            (aggregate: AggregateData) =>
                aggregate.aggregateName === name.trim()
        );

    const isNewAggregateNameInvalid = useMemo(() => {
        if (newAggregateName.trim() === "") return true;

        return aggNameExists(newAggregateName);
    }, [newAggregateName, aggregatesData]);

    useEffect(() => {
        fetchAggregates();
    }, []);
    return (
        <>
            <CustomisedToaster />
            <div className="inline-block w-full">
                <div className="flex justify-between items-center">
                    <h1 className={title()}>Aggregates</h1>
                    <Button
                        onPress={() => {
                            setNewAggregateName("");
                            onCreateOpen();
                        }}
                    >
                        Create New Aggregate
                    </Button>
                </div>
            </div>

            <Modal
                isOpen={isCreateOpen}
                onOpenChange={onCreateOpenChange}
                placement="top"
            >
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">
                                Create New Aggregate
                            </ModalHeader>
                            <ModalBody>
                                <Input
                                    autoFocus
                                    isRequired
                                    label="Aggregate Name"
                                    variant="bordered"
                                    type="text"
                                    isInvalid={isNewAggregateNameInvalid}
                                    value={newAggregateName}
                                    onValueChange={setNewAggregateName}
                                    errorMessage={
                                        newAggregateName.trim() === ""
                                            ? "Aggregate name cannot be blank"
                                            : "This aggregate name is already used"
                                    }
                                />
                            </ModalBody>
                            <ModalFooter>
                                <Button variant="flat" onPress={onClose}>
                                    Cancel
                                </Button>
                                <Button
                                    color="primary"
                                    isDisabled={isNewAggregateNameInvalid}
                                    onPress={async () => {
                                        await createNewAggregate();
                                        onClose();
                                    }}
                                >
                                    Create Aggregate
                                </Button>
                            </ModalFooter>
                        </>
                    )}
                </ModalContent>
            </Modal>

            <DeleteConfirmationModal
                isDeleteOpen={isDeleteOpen}
                onDeleteOpenChange={onDeleteOpenChange}
                selectedItemName={selectedAggregateName}
                onDeleteClicked={deleteAggregate}
                deleteType="Aggregate"
            />

            <div className="inline-block w-full text-center justify-center">
                <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
                    <Table
                        removeWrapper
                        className="w-full"
                        aria-label="List of aggregates"
                    >
                        <TableHeader>
                            <TableColumn className="text-center">
                                Aggregate Name
                            </TableColumn>
                            <TableColumn className="text-center">
                                Description
                            </TableColumn>
                            <TableColumn className="text-center">
                                Action
                            </TableColumn>
                        </TableHeader>
                        <TableBody>
                            {aggregatesData &&
                                aggregatesData.map(
                                    (elem: AggregateData, id: number) => (
                                        <TableRow key={id}>
                                            <TableCell className="text-center">
                                                {elem.aggregateName}
                                            </TableCell>
                                            <TableCell className="text-left">
                                                {elem.description}
                                            </TableCell>
                                            <TableCell className="text-center">
                                                <div className="flex justify-center items-center gap-2">
                                                    <Link
                                                        href={
                                                            "/edit-aggregate/?name=" +
                                                            elem.aggregateName
                                                        }
                                                    >
                                                        <Tooltip
                                                            content="Configure Aggregate"
                                                            placement="left"
                                                        >
                                                            <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
                                                                <EditIcon />
                                                            </span>
                                                        </Tooltip>
                                                    </Link>
                                                    <Spacer x={2} />
                                                    <Tooltip
                                                        color="danger"
                                                        content="Delete Aggregate"
                                                        placement="right"
                                                    >
                                                        <span
                                                            className="text-lg text-danger cursor-pointer active:opacity-50"
                                                            onClick={() => {
                                                                setSelectedAggregateName(
                                                                    elem.aggregateName
                                                                );
                                                                onDeleteOpen();
                                                            }}
                                                        >
                                                            <DeleteIcon />
                                                        </span>
                                                    </Tooltip>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    )
                                )}
                        </TableBody>
                    </Table>
                </section>
            </div>
        </>
    );
}
