part of 'fetch_bloc.dart';

// Fetch BLoC Events
abstract class FetchEvent {}

class StartFetching extends FetchEvent {
  String url;

  StartFetching(this.url);
}
