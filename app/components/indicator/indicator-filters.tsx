import { Chip } from "@nextui-org/chip";

export default function IndicatorFilters({
    indicatorFilters,
}: {
    indicatorFilters: Array<string>;
}) {
    return (
        <>
            {indicatorFilters.map((elem: string, id: number) => (
                <Chip key={id} color="primary" style={{ margin: "5px" }}>
                    {elem}
                </Chip>
            ))}
        </>
    );
}
