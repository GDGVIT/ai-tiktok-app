import 'package:aitok/features/videogen/bloc/video_generator_bloc.dart';
import 'package:aitok/features/videogen/views/download_video_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class VideoGenView extends StatefulWidget {
  static String routeName = '/videogen-screen';
  const VideoGenView({super.key});

  @override
  State<VideoGenView> createState() => _VideoGenViewState();
}

class _VideoGenViewState extends State<VideoGenView> {
  final TextEditingController scriptController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<VideoGeneratorBloc, VideoGeneratorState>(
      listener: (context, state) {
        if (state is VideoGeneratorError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                state.mgs ?? "Something went wrong!",
              ),
              backgroundColor: Colors.redAccent,
              behavior: SnackBarBehavior.floating,
            ),
          );
        } else if (state is TextResponseLoaded) {
          setState(() {
            scriptController.text = state.response.text;
          });
        } else if (state is VideoResponseLoaded) {
          Navigator.pushNamed(context, DownloadVideoView.routeName);
        }
      },
      builder: (context, state) {
        if (state is VideoGeneratorLoading) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        }
        return Scaffold(
          backgroundColor: Colors.black,
          appBar: AppBar(
            backgroundColor: Colors.black,
            title: const Text(
              "Enter your Script!",
              style: TextStyle(color: Colors.white),
            ),
            leading: IconButton(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(
                Icons.arrow_back,
                color: Colors.white,
              ),
            ),
          ),
          body: SafeArea(
            child: Center(
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: TextField(
                      controller: scriptController,
                      autofocus: true,
                      decoration: InputDecoration(
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(20),
                          borderSide: const BorderSide(
                            color: Colors.white,
                          ),
                        ),
                      ),
                      maxLines: 20,
                      style: const TextStyle(
                        color: Colors.white,
                      ),
                    ),
                  ),
                  const SizedBox(
                    height: 16,
                  ),
                  InkWell(
                    child: Container(
                      width: MediaQuery.of(context).size.width - 50,
                      height: 50,
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: Center(
                        child: Text(
                          "Generate Video",
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                      ),
                    ),
                    onTap: () {
                      if (state is VideoGeneratorInitial) {
                        BlocProvider.of<VideoGeneratorBloc>(context).add(
                          GetTextEvent(scriptController.text),
                        );
                      } else if (state is TextResponseLoaded) {
                        BlocProvider.of<VideoGeneratorBloc>(context).add(
                          GetVideoEvent(
                            text: state.response.text,
                            userId: state.response.userId,
                          ),
                        );
                      }
                    },
                  ),
                  const SizedBox(
                    height: 10,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
