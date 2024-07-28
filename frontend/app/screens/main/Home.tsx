import { View, Text, Button, StatusBar } from 'react-native'
import React from 'react'
import { styled }  from "nativewind"
import { AuthContext } from '@/context/AuthContext'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledButton = styled(Button)


const Home = () => {
    const { signOut } = React.useContext(AuthContext);

    return (
        <>
            <StatusBar barStyle="dark-content" backgroundColor="#ecf0f1" />
            <StyledView className="flex-1 items-center justify-center bg-[#ecf0f1]">
                <StyledButton title="Logout" onPress={() => signOut()} />
            </StyledView>
        </>
    )
}

export default Home