import 'package:get_it/get_it.dart';

import '../repositories/network_repo.dart';
import '../repositories/network_repo_interface.dart';
import 'network_config.dart';

final GetIt locator = GetIt.instance;

Future<void> setupLocator() async {
  ///---Network---
  locator.registerSingleton<NetworkConfig>(NetworkConfig());

  ///---Repos---
  locator.registerSingleton<NetworkRepoInterface>(
      NetworkRepo(networkProvider: locator<NetworkConfig>()));
}
