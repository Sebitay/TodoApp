import * as React from 'react';
import { StatusBar } from 'react-native';
import { withExpoSnack } from 'nativewind';
import * as SecureStore from 'expo-secure-store';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Login from "./screens/auth/Login";
import Register from "./screens/auth/Register";
import { LOGIN_URL, TEST_TOKEN_URL, REGISTER_URL } from "../constants/Urls";
import Home from './screens/main/Home';
import { AuthContext } from '@/context/AuthContext';

const Stack = createNativeStackNavigator();

function App() {
    const [state, dispatch] = React.useReducer(
        (prevState, action) => {
            switch (action.type) {
                case 'ERROR': 
                    return {
                        ...prevState,
                        message: 'Invalid username or password.'
                    };
                case 'RESTORE_TOKEN': 
                    return {
                        ...prevState,
                        userToken: action.token,
                        isLoading: false,
                        message: ''
                    };
                case 'SIGN_IN':
                    return {
                        ...prevState,
                        isSignout: false,
                        userToken: action.token,
                        message: ''
                    };
                case 'SIGN_OUT':
                    return {
                        ...prevState,
                        isSignout: true,
                        userToken: null,
                        message: ''
                    };
                default:
                    return prevState;
            }
        },
        {   
            message: '',
            isLoading: true,
            isSignout: false,
            userToken: null,
        }
    );

    React.useEffect(() => {
        const bootstrapAsync = async () => {
            let userToken;
    
            try {
                userToken = await SecureStore.getItemAsync('userToken');
            } catch (e) {
                // Restoring token failed
            }

            if (userToken) {
                const res = await fetch(TEST_TOKEN_URL, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${userToken}`
                    }
                });
                if (res.status === 200) {
                    dispatch({ type: 'RESTORE_TOKEN', token: userToken });
                    return;
                }
            }
            dispatch({ type: 'SIGN_OUT' });
        };
    
        bootstrapAsync();
    }, []);

    const authContext = React.useMemo(() => ({
        signIn: async ({username, password}) => {
            const res = await fetch(LOGIN_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, password})
            }).then(res => res.json());
            if (res.token) {
                await SecureStore.setItemAsync('userToken', res.token);
                dispatch({ type: 'SIGN_IN', token: res.token });
            } else {
                dispatch({ type: 'ERROR' })
            }
        },

        signOut: () => {
            dispatch({ type: 'SIGN_OUT' });
            SecureStore.deleteItemAsync('userToken');
        },

        signUp: async ({username, email, password}) => {
            const res = await fetch(REGISTER_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username, email, password})
            }).then(res => res.json());
            if (res.token) {
                await SecureStore.setItemAsync('userToken', res.token);
                dispatch({ type: 'SIGN_IN', token: res.token });
            }
        },
    }), []);
    
    return (
        <AuthContext.Provider value={authContext}>
                <Stack.Navigator screenOptions={{headerShown: false, backgroundColor: "#ecf0f1"}}>
                    {state.userToken == null ? (
                        <>
                            <Stack.Screen 
                                name="Login" 
                                component={Login} 
                                initialParams={{ text: state.message }}
                            />
                            <Stack.Screen 
                                name="Register" 
                                component={Register} 
                                initialParams={{ text: {username: "", email: "", password: "", rePassword: ""} }}
                            />
                        </>
                    ) : (
                        <Stack.Screen name="Home" component={Home} />
                    )}
                </Stack.Navigator>
        </AuthContext.Provider>
    );
}

export default withExpoSnack(App);