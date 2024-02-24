import 'package:aitok/features/videofetch/bloc/fetch_bloc.dart';
import 'package:aitok/features/videofetch/bloc/timer_bloc.dart';
import 'package:aitok/features/videofetch/views/timer_page_view.dart';
import 'package:aitok/features/videogen/bloc/video_generator_bloc.dart';
import 'package:aitok/features/videogen/views/download_video_view.dart';
import 'package:aitok/features/videogen/views/videogen_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'core/service_locator.dart';
import 'features/home/views/homepage_view.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  //dependency Injection
  await setupLocator();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => VideoGeneratorBloc(),
      child: MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        // home: const MyHomePage(),
        initialRoute: MyHomePage.routeName,
        routes: {
          MyHomePage.routeName: (ctx) => const MyHomePage(),
          VideoGenView.routeName: (ctx) => const VideoGenView(),
          DownloadVideoView.routeName: (ctx) => const DownloadVideoView(),
          TimerPage.routeName: (ctx) => MultiBlocProvider(
                providers: [
                  BlocProvider(
                    create: (context) => TimerBloc(),
                  ),
                  BlocProvider(
                    create: (context) => FetchBloc(),
                  ),
                ],
                child: TimerPage(),
              ),
        },
      ),
    );
  }
}
