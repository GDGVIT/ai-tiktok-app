import 'dart:async';

import 'package:flutter_bloc/flutter_bloc.dart';

part './timer_state.dart';
part 'timer_event.dart';

// Timer BLoC
class TimerBloc extends Bloc<TimerEvent, TimerState> {
  late Timer _timer;
  int _timerDurationSeconds = 120; // 2 minutes

  TimerBloc() : super(TimerInitial());

  Stream<TimerState> mapEventToState(TimerEvent event) async* {
    if (event is StartTimer) {
      yield* _startTimer();
    } else if (event is Tick) {
      yield* _tick();
    }
  }

  Stream<TimerState> _startTimer() async* {
    yield TimerRunning(_timerDurationSeconds);

    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      add(Tick());
    });
  }

  Stream<TimerState> _tick() async* {
    _timerDurationSeconds--;

    if (_timerDurationSeconds <= 0) {
      _timer.cancel();
      yield TimerFinished();
    }
  }

  @override
  Future<void> close() {
    _timer.cancel();
    return super.close();
  }
}
