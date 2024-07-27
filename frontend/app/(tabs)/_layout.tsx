import { View, Text, StatusBar } from 'react-native'
import { Tabs, Slot } from 'expo-router'
import { styled } from 'nativewind'
import React from 'react'

const StyledView = styled(View)

const _layout = () => {

    return (
        <StyledView className='h-full'>
            <Tabs>
                <Tabs.Screen 
                    name="index"
                    options ={{headerShown: false, title: 'Home'}}
                    
                />
                <Tabs.Screen 
                    name="settings" 
                    options ={{headerShown: false, title: 'Settings'}}
                />
            </Tabs>
        </StyledView>
    )
}

export default _layout