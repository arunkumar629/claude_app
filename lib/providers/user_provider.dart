import 'package:flutter/foundation.dart';
import '../models/user.dart';

class UserProvider with ChangeNotifier {
  final List<User> _users = [];

  List<User> get users => List.unmodifiable(_users);

  void addUser(String name, int age) {
    final user = User(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: name,
      age: age,
    );
    _users.add(user);
    notifyListeners();
  }

  void removeUser(String id) {
    _users.removeWhere((user) => user.id == id);
    notifyListeners();
  }

  void clearAll() {
    _users.clear();
    notifyListeners();
  }
}
