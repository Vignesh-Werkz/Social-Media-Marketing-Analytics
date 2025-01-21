import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
} from "@nextui-org/modal";
import { Select, SelectItem } from "@nextui-org/select";
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import { Dispatch, SetStateAction } from "react";
import { SharedSelection } from "@nextui-org/system";
import { AggregateData } from "../aggregate-config/types";

export default function MakeIndicatorModal({
    isMakeOpen,
    onMakeOpenChange,
    newIndicatorName,
    setNewIndicatorName,
    newIndicatorNameIsEmpty,
    newIndicatorNameExists,
    newIndicatorAggregate,
    setNewIndicatorAggregate,
    aggregateList,
    newIndicatorFilters,
    setNewIndicatorFilters,
    createNewIndicator,
    isNewIndicatorInvalid,
}: {
    isMakeOpen: boolean;
    onMakeOpenChange: () => void;
    newIndicatorName: string;
    setNewIndicatorName: Dispatch<SetStateAction<string>>;
    newIndicatorNameIsEmpty: boolean;
    newIndicatorNameExists: boolean;
    newIndicatorAggregate: SharedSelection;
    setNewIndicatorAggregate: Dispatch<SetStateAction<SharedSelection>>;
    aggregateList: Array<AggregateData>;
    newIndicatorFilters: string;
    setNewIndicatorFilters: Dispatch<SetStateAction<string>>;
    createNewIndicator: () => Promise<void>;
    isNewIndicatorInvalid: boolean;
}) {
    return (
        <Modal
            isOpen={isMakeOpen}
            onOpenChange={onMakeOpenChange}
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
                                        ? "Indicator name cannot be empty"
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
                                placeholder="Type your filters separated by semi-colons ;"
                                variant="bordered"
                                value={newIndicatorFilters}
                                onValueChange={setNewIndicatorFilters}
                            />
                        </ModalBody>
                        <ModalFooter>
                            <Button variant="flat" onPress={onClose}>
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
                        </ModalFooter>
                    </>
                )}
            </ModalContent>
        </Modal>
    );
}
