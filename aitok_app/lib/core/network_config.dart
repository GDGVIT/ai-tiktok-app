import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';

import 'constants.dart';

class NetworkConfig {
  // late final Dio _dio;
  //
  // NetworkConfig() {
  //   _dio = Dio(
  //     BaseOptions(
  //       baseUrl: AppConstants.baseUrl,
  //     ),
  //   );
  //   initializeInterceptors();
  // }
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: AppConstants.baseUrl,
    ),
  );

  //Get Req
  Future<Response> getRequest(String endPoint) async {
    Response response;

    debugPrint(endPoint);

    try {
      response = await _dio.get(endPoint);
    } on DioException catch (e) {
      debugPrint(e.message);
      throw Exception(e.message);
    }

    return response;
  }

  //Post Req
  Future<Response> postRequest(
      String endPoint, Map<String, String> body) async {
    Response response;

    try {
      response = await _dio.post(endPoint, data: body);
      debugPrint(response.data.toString());
    } catch (e) {
      throw Exception(e);
    }

    return response;
  }

  initializeInterceptors() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (request, requestInterceptorHandler) {
          debugPrint("${request.method} ${request.path}");
          debugPrint("${request.data} ${request.uri}");
        },
        onResponse: (response, requestInterceptorHandler) {
          debugPrint(response.data);
        },
      ),
    );
  }
}
