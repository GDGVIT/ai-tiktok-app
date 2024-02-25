import 'dart:io'; // Import the dart:io package

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:video_player/video_player.dart';

import '../../../core/constants.dart';
import '../bloc/video_generator_bloc.dart';

class DownloadVideoView extends StatefulWidget {
  static String routeName = '/video-download-screen';
  const DownloadVideoView({super.key});

  @override
  State<DownloadVideoView> createState() => _DownloadVideoViewState();
}

String? videoUrl =
    "https://reelgen-wandering-resonance-2223.fly.dev/092874a/video/video.mp4";
Dio _dio = Dio();

Future<void> _downloadVideo(String url, BuildContext context) async {
  try {
    final Directory appDocDir = await getApplicationDocumentsDirectory();
    final String filePath = '${appDocDir.path}/video.mp4';

    // Show download dialog
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return const AlertDialog(
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 16),
              Text('Downloading...'),
            ],
          ),
        );
      },
    );

    await _dio.download(url, filePath);

    // Optionally, you can perform additional actions after the download is complete
    print('Video downloaded successfully! File saved at: $filePath');

    // Close the download dialog
    Navigator.of(context).pop();

    // Optionally, you can display a success message or perform other actions
    // after the download is complete.
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Video downloaded successfully!'),
      ),
    );
  } catch (e) {
    // Close the download dialog in case of an error
    Navigator.of(context).pop();

    print('Error downloading video: $e');
    // Optionally, you can display an error message or perform other actions
    // in case of an error.
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Error downloading video: $e'),
        backgroundColor: Colors.red,
      ),
    );
  }
}

Future<void> download(BuildContext context) async {
  debugPrint("download");
  await Permission.storage.request();
  if (await Permission.storage.status.isGranted) {
    await _downloadVideo(videoUrl!, context);
    // await _downloadVideo(
    //     "https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4",
    //     context);
  } else {
    print('Storage permission denied');
  }
}

class _DownloadVideoViewState extends State<DownloadVideoView> {
  late VideoPlayerController _controller;
  @override
  void initState() {
    videoUrl =
        '${AppConstants.baseUrl}/${BlocProvider.of<VideoGeneratorBloc>(context).videoUrl}';
    super.initState();
    _controller = VideoPlayerController.networkUrl(
      Uri.parse(
        videoUrl!,
        // 'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4'
      ),
    )..initialize().then(
        (_) {
          // Ensure the first frame is shown after the video is initialized, even before the play button has been pressed.
          setState(() {
            _controller.play();
          });
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
          ),
        ),
      ),
      body: Center(
        child: _controller.value.isInitialized
            ? GestureDetector(
                child: AspectRatio(
                  aspectRatio: _controller.value.aspectRatio,
                  child: VideoPlayer(_controller),
                ),
                onTap: () {
                  setState(() {
                    _controller.value.isPlaying
                        ? _controller.pause()
                        : _controller.play();
                  });
                },
              )
            : const Center(
                child: Text(
                  "Looking up for the video!",
                  style: TextStyle(color: Colors.white),
                ),
              ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => download(context),
        child: const Icon(
          Icons.download,
        ),
      ),
    );
  }
}
