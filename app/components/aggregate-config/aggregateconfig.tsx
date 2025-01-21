import { ModelBox } from "@/components/aggregate-config/modelbox";
import { AggregateData, ModelData } from "./types";

export const AggregateConfig = ({
    aggregateData,
    updateModelWeightsData,
}: {
    aggregateData: AggregateData;
    updateModelWeightsData: (data: ModelData) => void;
}) => {
    return (
        <div className="flex">
            {aggregateData &&
                aggregateData.weights.map((elem: ModelData, i: number) => (
                    <ModelBox
                        key={i}
                        modelData={elem}
                        updateModelWeightsData={updateModelWeightsData}
                    />
                ))}
        </div>
    );
};
