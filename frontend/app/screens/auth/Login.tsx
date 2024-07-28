import { View, Text, Button, StatusBar, TextInput } from 'react-native'
import { AuthContext } from '@/context/AuthContext'
import { styled, withExpoSnack }  from "nativewind"
import React, { useEffect } from 'react'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledButton = styled(Button)
const StyledTextInput = styled(TextInput)

const Login = ({ route, navigation }: {route: any, navigation: any}) => {

  const { text } = route.params


  const [username, setUsername] = React.useState<string>('')
  const [password, setPassword] = React.useState<string>('')

  const { signIn } = React.useContext(AuthContext)

  return (
    <>
      <StatusBar barStyle="dark-content" backgroundColor="#ecf0f1" />
      <StyledView className="flex-1 items-center justify-center h-full space-y-5 bg-[#ecf0f1]">
          <StyledText className="text-red-500">{text}</StyledText>
          <StyledText className='text-xl font-bold'>Login</StyledText>
          <StyledTextInput placeholder="Username" value={username} onChangeText={setUsername} className="w-2/3 h-[45] border-2 border-gray-500 rounded-xl p-2" autoCapitalize='none'/>
          <StyledTextInput placeholder="Password" value={password} onChangeText={setPassword} className="w-2/3 h-[45] border-2 border-gray-500 rounded-xl p-2 mb-5" secureTextEntry autoCapitalize='none'/>
          <StyledButton 
            title="Login" 
            onPress={() => {
              signIn( {username, password}); 
              navigation.setParams({text: 'Invalid username or password'})}}
          />
      </StyledView>
    </>
  )
}

export default Login