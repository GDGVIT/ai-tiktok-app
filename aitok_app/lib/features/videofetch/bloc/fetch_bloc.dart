import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:flutter/cupertino.dart';

import '../../../core/service_locator.dart';
import '../../../repositories/network_repo_interface.dart';

part 'fetch_event.dart';
part 'fetch_state.dart';

// Fetch BLoC
class FetchBloc extends Bloc<FetchEvent, FetchState> {
  final remoteRepo = locator<NetworkRepoInterface>();
  late Timer _timer;
  final int _retryIntervalSeconds = 30; // Replace with your desired URL

  FetchBloc() : super(FetchInitial()) {
    on<StartFetching>((event, emit) async {
      _timer =
          Timer.periodic(Duration(seconds: _retryIntervalSeconds), (timer) {
        _fetchData(event.url);
      });
    });
  }

  Future<void> _fetchData(String url) async {
    debugPrint("Fetching Video");
    try {
      final response = await remoteRepo.fetchVideoUrl(url);

      if (response == true) {
        _timer.cancel();
        emit(FetchSuccess());
      }
    } catch (error) {
      // Handle errors or retries if needed
      debugPrint("Error fetching data: $error");
    }
  }

  @override
  Future<void> close() {
    _timer.cancel();
    return super.close();
  }
}
