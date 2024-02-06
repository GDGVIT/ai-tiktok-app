part of 'video_generator_bloc.dart';

abstract class VideoGeneratorState extends Equatable {
  const VideoGeneratorState();
}

class VideoGeneratorInitial extends VideoGeneratorState {
  @override
  List<Object> get props => [];
}

class VideoGeneratorLoading extends VideoGeneratorState {
  @override
  List<Object> get props => [];
}

class VideoGeneratorError extends VideoGeneratorState {
  final String? mgs;

  const VideoGeneratorError({this.mgs = "Something went wrong"});

  @override
  List<Object> get props => [];
}

class TextResponseLoaded extends VideoGeneratorState {
  final TextResponseModel response;

  const TextResponseLoaded(this.response);

  @override
  List<Object> get props => [];
}

class VideoResponseLoaded extends VideoGeneratorState {
  final String url;

  const VideoResponseLoaded(this.url);

  @override
  List<Object> get props => [];
}
