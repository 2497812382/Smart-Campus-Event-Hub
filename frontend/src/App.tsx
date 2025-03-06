import React, { useState, useEffect } from 'react';
import axios from 'axios';

// 1. 定义 Task 接口（确保字段与 Django 返回的 JSON 数据匹配）
interface Task {
  id: number;
  title: string;
  completed: boolean;
}

function App() {
  // 2. 关键：使用泛型指定状态类型
  const [tasks, setTasks] = useState<Task[]>([]); // 声明 tasks 是 Task 数组类型

  // 获取任务列表
  useEffect(() => {
    // 3. axios.get 使用泛型指定响应数据类型
    axios.get<Task[]>('http://localhost:8000/api/tasks/') // 明确返回的数据类型
      .then(res => setTasks(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Todo List</h1>
      <ul>
        {tasks.map(task => (
          // 现在 task.id 能被 TypeScript 正确识别
          <li key={task.id}>
            {task.title} - {task.completed ? "✅" : "❌"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
