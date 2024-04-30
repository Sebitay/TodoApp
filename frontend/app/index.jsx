import { StatusBar } from 'expo-status-bar';
import { Text, View } from 'react-native';
import { Link } from 'expo-router';

export default function App() {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-3xl">Todo App</Text>
      <StatusBar style="auto" />
      <Link href="/todos" className="text-blue-500">Todos</Link>
    </View>
  );
}
