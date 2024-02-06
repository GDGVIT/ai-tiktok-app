import 'dart:convert';

class TextResponseModel {
  final String text;
  final String userId;

  TextResponseModel({
    required this.text,
    required this.userId,
  });

  TextResponseModel copyWith({
    String? text,
    String? userId,
  }) =>
      TextResponseModel(
        text: text ?? this.text,
        userId: userId ?? this.userId,
      );

  factory TextResponseModel.fromRawJson(String str) =>
      TextResponseModel.fromJson(json.decode(str));

  String toRawJson() => json.encode(toJson());

  factory TextResponseModel.fromJson(Map<String, dynamic> json) =>
      TextResponseModel(
        text: json["text"],
        userId: json["user_id"],
      );

  Map<String, dynamic> toJson() => {
        "text": text,
        "user_id": userId,
      };
}
