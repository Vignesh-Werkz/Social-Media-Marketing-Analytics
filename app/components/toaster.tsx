import { Toaster } from "sonner";
import { useTheme } from "next-themes";

export default function CustomisedToaster() {
    const { theme } = useTheme();

    return (
        <Toaster
            position="top-center"
            theme={theme! === "dark" ? "dark" : "light"}
            offset="100px"
            richColors
        />
    );
}
