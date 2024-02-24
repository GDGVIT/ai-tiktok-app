import 'package:aitok/core/network_config.dart';
import 'package:aitok/models/response_model.dart';

import 'network_repo_interface.dart';

class NetworkRepo implements NetworkRepoInterface {
  final NetworkConfig networkProvider;

  const NetworkRepo({required this.networkProvider});

  @override
  Future<TextResponseModel> getTextResponse(String text) async {
    final body = {"text": text};
    try {
      final response = await networkProvider.postRequest("/text", body);
      if (response.statusCode == 200) {
        return TextResponseModel.fromJson(response.data);
      } else {
        throw Exception("Failed to get text");
      }
    } catch (e) {
      throw Exception("Something went wrong!");
    }
  }

  @override
  Future<String> getVideoResponse(String text, String userId) async {
    final body = {"text": text, "user_id": userId};
    try {
      final response = await networkProvider.postRequest("/edittext", body);
      if (response.statusCode == 200) {
        return response.data["videoUrl"];
      } else {
        throw Exception("Failed to get text");
      }
    } catch (e) {
      throw Exception("Something went wrong!");
    }
  }

  @override
  Future<bool> fetchVideoUrl(String url) async {
    try {
      final response = await networkProvider.getRequest('/$url');
      if (response.statusCode == 200) {
        return true;
      } else {
        throw Exception("Failed to get text");
      }
    } catch (e) {
      throw Exception("Something went wrong!");
    }
  }
}
