part of 'timer_bloc.dart';

// Timer BLoC Events
abstract class TimerEvent {}

class StartTimer extends TimerEvent {}

class Tick extends TimerEvent {}
