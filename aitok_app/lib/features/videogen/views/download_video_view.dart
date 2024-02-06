import 'package:aitok/core/constants.dart';
import 'package:aitok/features/videogen/bloc/video_generator_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class DownloadVideoView extends StatefulWidget {
  static String routeName = '/video-download-screen';
  const DownloadVideoView({super.key});

  @override
  State<DownloadVideoView> createState() => _DownloadVideoViewState();
}

class _DownloadVideoViewState extends State<DownloadVideoView> {
  @override
  Widget build(BuildContext context) {
    String? videoUrl =
        '${AppConstants.baseUrl}${BlocProvider.of<VideoGeneratorBloc>(context).videoUrl}';
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
        child: Text(videoUrl),
      ),
    );
  }
}
