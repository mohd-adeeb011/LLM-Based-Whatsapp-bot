
'''
searchforDishesTool = Tool(
        name='searchforDishes',
        func= searchforDishes,
        description="Useful when u want you want to fetch restaurant, dish,portion sizing, price, address of restaurant for user. If user need anything, return with Restaurant Name, Dish Name, Portion Sizing, Price and Address")

        FinalOrderTool=Tool(
            name='PlaceFinalOrderr',
            func=PlaceFinalOrder,
            description="Useful for storing the Final order of the user. It will not return any significant information but, this has to be used when user decided to store the information of the order to finally place the order. Once this function is used, you have to infrom the user that, your order has been placed."
        )
        getFinalOrderTool=Tool(
            name="getFinalOrder",
            func=getFinalOrder,
            description="Useful for fetching the order placed by the user."
        )
        tools = [searchforDishesTool,FinalOrderTool,getFinalOrderTool]
        llm_with_tools = llm.bind_tools(tools)
        MEMORY_KEY = "chat_history"
        
        chat_history = []
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a Food Ordering agent, which conversates with user what they want to eat. Your work is to call different functions or tools to do different task like asking user what they want to eat, giving relevant choices, makeing temperary order, confirming order. So, your flow will be first asking the user what they want to eat then giving them choices accoring to the user requirement, then you have to ask what they want to order, when the tell you what they want to order, you have to store the order in the temperary memory, and add or subtract from the order if user wants, and finally place the order after asking to user and tell the final order to user what they have ordered and store the order in the orderFood function.",
                ),
                MessagesPlaceholder(variable_name=MEMORY_KEY),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        result = agent_executor.invoke({"input": incoming_msg, "chat_history": chat_history})
        chat_history.extend(
            [
                HumanMessage(content=incoming_msg),
                AIMessage(content=result["output"]),
            ]
        )
        agent_executor.invoke({"input": incoming_msg, "chat_history": chat_history})
        # print(response)
        respond(result["output"],receiver_contact,froms)

'''