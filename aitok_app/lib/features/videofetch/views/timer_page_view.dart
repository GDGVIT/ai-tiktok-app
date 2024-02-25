import 'package:aitok/features/videogen/views/download_video_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../bloc/fetch_bloc.dart';
import '../widget/countdown_widget.dart';

// Timer Page
class TimerPage extends StatefulWidget {
  static String routeName = '/video-timer-screen';

  TimerPage({super.key});

  @override
  State<TimerPage> createState() => _TimerPageState();
}

class _TimerPageState extends State<TimerPage> {
  String? videoUrl;

  @override
  Widget build(BuildContext context) {
    videoUrl = ModalRoute.of(context)?.settings.arguments as String;
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "Timer Page",
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
      body: BlocConsumer<FetchBloc, FetchState>(
        builder: (context, state) {
          debugPrint(state.toString());
          if (state is FetchInitial) {
            context.read<FetchBloc>().add(StartFetching(videoUrl!));
          }
          return CountdownWidget();
        },
        listener: (BuildContext context, FetchState state) {
          if (state is FetchSuccess) {
            debugPrint("Timer Finished");
            Navigator.pushNamed(context, DownloadVideoView.routeName);
            // Implement your navigation logic to a different page here
            // For example: Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => AnotherPage()));
          }
        },
      ),
    );
  }
}
