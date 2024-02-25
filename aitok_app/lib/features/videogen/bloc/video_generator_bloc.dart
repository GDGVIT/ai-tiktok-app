import 'package:aitok/models/response_model.dart';
import 'package:aitok/repositories/network_repo_interface.dart';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/cupertino.dart';

import '../../../core/service_locator.dart';

part 'video_generator_event.dart';
part 'video_generator_state.dart';

class VideoGeneratorBloc
    extends Bloc<VideoGeneratorEvent, VideoGeneratorState> {
  final remoteRepo = locator<NetworkRepoInterface>();
  String? videoUrl;

  VideoGeneratorBloc() : super(VideoGeneratorInitial()) {
    on<GetTextEvent>((event, emit) async {
      emit(VideoGeneratorLoading());
      try {
        final response = await remoteRepo.getTextResponse(event.text);
        emit(TextResponseLoaded(response));
      } catch (e) {
        debugPrint(e.toString());
        emit(const VideoGeneratorError(mgs: "Something went wrong!"));
        emit(VideoGeneratorInitial());
      }
    });

    //getVideo
    on<GetVideoEvent>((event, emit) async {
      try {
        emit(VideoGeneratorLoading());
        final response =
            await remoteRepo.getVideoResponse(event.text, event.userId);
        videoUrl = response;
        emit(VideoResponseLoaded(response));
      } catch (e) {
        emit(const VideoGeneratorError(mgs: "Something went wrong!"));
        emit(VideoGeneratorInitial());
      }
    });
  }
}
