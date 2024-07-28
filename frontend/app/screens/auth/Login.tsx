import { View, Text, TouchableOpacity, StatusBar, TextInput } from 'react-native'
import { AuthContext } from '@/context/AuthContext'
import { styled }  from "nativewind"
import React from 'react'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledTouchableOpacity = styled(TouchableOpacity)
const StyledTextInput = styled(TextInput)

const Login = ({ route, navigation }: {route: any, navigation: any}) => {

  const { text } = route.params


  const [username, setUsername] = React.useState<string>('')
  const [password, setPassword] = React.useState<string>('')

  const { signIn } = React.useContext(AuthContext)

  return (
    <>
      <StatusBar barStyle="dark-content" backgroundColor="white" />
      <StyledView className="flex-1 items-center justify-center h-full space-y-5 bg-white">
          <StyledText className="text-red-500">{text}</StyledText>
          <StyledText className='text-xl font-bold'>Login</StyledText>
          <StyledTextInput placeholder="Username" value={username} onChangeText={setUsername} className="w-2/3 h-[45] border-2 border-gray-500 rounded-xl p-2" autoCapitalize='none'/>
          <StyledTextInput placeholder="Password" value={password} onChangeText={setPassword} className="w-2/3 h-[45] border-2 border-gray-500 rounded-xl p-2" secureTextEntry autoCapitalize='none'/>
          <StyledTouchableOpacity 
            className="bg-blue-500 p-2 rounded-xl w-2/3"
            onPress={() => {
              signIn({ username, password }); 
              navigation.setParams({text: 'Invalid username or password'})}}
          >
            <StyledText className="text-white bg-blue-500 rounded-xl text-center text-xl font-bold">Login</StyledText>
          </StyledTouchableOpacity>
          <StyledTouchableOpacity onPress={() => navigation.navigate('Register')}>
            <StyledText className="text-blue-500">Don't have an account?</StyledText>
          </StyledTouchableOpacity>
      </StyledView>
    </>
  )
}

export default Login