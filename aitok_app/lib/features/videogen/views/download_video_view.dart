import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:video_player/video_player.dart';

import '../../../core/constants.dart';
import '../bloc/video_generator_bloc.dart';

class DownloadVideoView extends StatefulWidget {
  static String routeName = '/video-download-screen';
  const DownloadVideoView({super.key});

  @override
  State<DownloadVideoView> createState() => _DownloadVideoViewState();
}

String? videoUrl;

class _DownloadVideoViewState extends State<DownloadVideoView> {
  late VideoPlayerController _controller;

  // @override
  // void initState() {
  //   videoUrl =
  //       '${AppConstants.baseUrl}/${BlocProvider.of<VideoGeneratorBloc>(context).videoUrl}';
  //   _controller = VideoPlayerController.networkUrl(Uri.parse(
  //       "https://reelgen-wandering-resonance-2223.fly.dev/571c921/video/video.mp4"));
  //   super.initState();
  // }
  @override
  void initState() {
    videoUrl =
        '${AppConstants.baseUrl}/${BlocProvider.of<VideoGeneratorBloc>(context).videoUrl}';
    super.initState();
    _controller = VideoPlayerController.networkUrl(
      Uri.parse(
        videoUrl!,
      ),
    )..initialize().then(
        (_) {
          // Ensure the first frame is shown after the video is initialized, even before the play button has been pressed.
          setState(() {});
        },
      );
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(videoUrl);
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "Your Video Created!",
          style: TextStyle(color: Colors.white),
        ),
        leading: IconButton(
            onPressed: () => Navigator.pop(context),
            icon: const Icon(
              Icons.arrow_back_ios,
              color: Colors.white,
            )),
      ),
      body: Center(
        child: _controller.value.isInitialized
            ? AspectRatio(
                aspectRatio: _controller.value.aspectRatio,
                child: VideoPlayer(_controller),
              )
            : const Center(
                child: Text(
                  "Error while loading video!",
                  style: TextStyle(color: Colors.white),
                ),
              ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            _controller.value.isPlaying
                ? _controller.pause()
                : _controller.play();
          });
        },
        child: Icon(
          _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
        ),
      ),
    );
  }
}
