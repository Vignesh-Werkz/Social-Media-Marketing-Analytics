from concurrent import futures
import grpc
import da_dv_pb2
import da_dv_pb2_grpc
from dataanalysis.data_analysis import DataAnalysis

class RecalculateIndicator(da_dv_pb2_grpc.RecalculateIndicatorServicer):
    def __init__(self):
        self.da = DataAnalysis()
    def RecalculateIndicator(self, request, context):
        print("Received indicator: " + request.object_name)
        self.da.execute(update_type='all', indicator_names=[request.object_name])
        return da_dv_pb2.RecalculateResponse(result='Triggered recalculation for indicator: %s' % request.object_name)

class RecalculateAggregate(da_dv_pb2_grpc.RecalculateAggregateServicer):
    def RecalculateAggregate(self, request, context):
        print("Received aggregate: " + request.object_name)
        da = DataAnalysis()
        da.execute(update_type='all', aggregate_name=request.object_name)
        return da_dv_pb2.RecalculateResponse(result='Triggrered recalculation for aggregate: %s' % request.object_name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    da_dv_pb2_grpc.add_RecalculateIndicatorServicer_to_server(RecalculateIndicator(), server)
    da_dv_pb2_grpc.add_RecalculateAggregateServicer_to_server(RecalculateAggregate(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    print("Starting DAServer...")
    serve()
