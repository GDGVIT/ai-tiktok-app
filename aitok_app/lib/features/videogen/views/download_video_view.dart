import 'package:aitok/core/constants.dart';
import 'package:aitok/features/videogen/bloc/video_generator_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:video_player/video_player.dart';

class DownloadVideoView extends StatefulWidget {
  static String routeName = '/video-download-screen';
  const DownloadVideoView({super.key});

  @override
  State<DownloadVideoView> createState() => _DownloadVideoViewState();
}

String? videoUrl;

class _DownloadVideoViewState extends State<DownloadVideoView> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    videoUrl =
        '${AppConstants.baseUrl}/${BlocProvider.of<VideoGeneratorBloc>(context).videoUrl}';
    _controller = VideoPlayerController.networkUrl(Uri.parse(videoUrl!))
      ..initialize().then((_) {
        // Ensure the first frame is shown after the video is initialized, even before the play button has been pressed.
        setState(() {});
      });
    super.initState();
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
            : Container(),
      ),
    );
  }
}
