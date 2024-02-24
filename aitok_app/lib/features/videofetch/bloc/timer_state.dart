part of '../../videofetch/bloc/timer_bloc.dart';

// Timer BLoC States
abstract class TimerState {}

class TimerInitial extends TimerState {}

class TimerRunning extends TimerState {
  final int seconds;

  TimerRunning(this.seconds);
}

class TimerFinished extends TimerState {}
