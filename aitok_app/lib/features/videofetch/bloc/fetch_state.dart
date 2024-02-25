part of 'fetch_bloc.dart';

// Fetch BLoC States
abstract class FetchState {}

class FetchInitial extends FetchState {}

class FetchSuccess extends FetchState {}

class Fetching extends FetchState {}
