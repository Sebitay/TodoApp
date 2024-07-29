import { View, ScrollView, Text, Button, StatusBar } from 'react-native'
import React from 'react'
import { styled }  from "nativewind"
import { AuthContext } from '@/context/AuthContext'
import { DateBar, TodoListItem }from '@/components'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledButton = styled(Button)


const Daily = () => {
    const { signOut } = React.useContext(AuthContext);
    const todos = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty']

    const [date, setDate] = React.useState<Date>(new Date())

    return (
        <>
            <StatusBar barStyle="dark-content" backgroundColor="white" />
                <DateBar date={date} setDate={setDate}/>
            <ScrollView>
                <StyledView className="flex-1 items-center justify-center bg-[#ecf0f1]" >
                    {todos.map((todo, index) => (
                        <TodoListItem key={index} text={todo} id={index} />
                    ))}
                    <StyledButton title="Logout" onPress={() => signOut()} />
                </StyledView>
            </ScrollView>
        </>
    )
}

export default Daily