import {
    Modal,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
} from "@nextui-org/modal";
import { Button } from "@nextui-org/button";

export default function DeleteConfirmationModal({
    isDeleteOpen,
    onDeleteOpenChange,
    selectedItemName,
    onDeleteClicked,
    deleteType,
}: {
    isDeleteOpen: boolean;
    onDeleteOpenChange: () => void;
    selectedItemName: string;
    onDeleteClicked: () => Promise<void>;
    deleteType: string;
}) {
    return (
        <Modal isOpen={isDeleteOpen} onOpenChange={onDeleteOpenChange}>
            <ModalContent>
                {(onClose) => (
                    <>
                        <ModalHeader className="flex flex-col gap-1">
                            Delete {selectedItemName}?
                        </ModalHeader>
                        <ModalBody>
                            <p>This action cannot be undone.</p>
                        </ModalBody>
                        <ModalFooter>
                            <Button variant="light" onPress={onClose}>
                                Go Back
                            </Button>
                            <Button
                                color="danger"
                                onPress={async () => {
                                    await onDeleteClicked();
                                    onClose();
                                }}
                            >
                                Delete {deleteType}
                            </Button>
                        </ModalFooter>
                    </>
                )}
            </ModalContent>
        </Modal>
    );
}
