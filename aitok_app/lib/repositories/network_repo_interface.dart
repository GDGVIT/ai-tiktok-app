import 'package:aitok/models/response_model.dart';

abstract class NetworkRepoInterface {
  Future<TextResponseModel> getTextResponse(String text);
  Future<String> getVideoResponse(String text, String userId);
}
