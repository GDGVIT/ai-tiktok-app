part of 'video_generator_bloc.dart';

abstract class VideoGeneratorEvent extends Equatable {
  const VideoGeneratorEvent();
}

class GetTextEvent extends VideoGeneratorEvent {
  final String text;

  const GetTextEvent(this.text);

  @override
  List<Object> get props => [];
}

class GetVideoEvent extends VideoGeneratorEvent {
  final String text;
  final String userId;

  const GetVideoEvent({required this.text, required this.userId});

  @override
  List<Object> get props => [];
}

class DownloadVideoEvent extends VideoGeneratorEvent {
  final String url;

  const DownloadVideoEvent(this.url);

  @override
  List<Object> get props => [];
}
