export interface ResultsData {
    date: string;
    average_score: number;
}

export interface IndicatorData {
    indicatorName: string;
    filters: Array<string>;
    aggregateName: string;
    resultsByDay: Array<ResultsData>;
    resultsByMonth: Array<ResultsData>;
}
