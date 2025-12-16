import customtkinter as ctk
import json
from datetime import datetime
from typing import List, Dict
import os

class TodoItem:
    """待办事项数据模型"""
    def __init__(self, text: str, completed: bool = False, created_at: str = None):
        self.text = text
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            text=data["text"],
            completed=data["completed"],
            created_at=data.get("created_at")
        )


class TodoListApp(ctk.CTk):
    """Google 风格的待办事项应用"""

    def __init__(self):
        super().__init__()

        # 配置主窗口
        self.title("Todo List")
        self.geometry("500x700")

        # 设置 Google Material Design 风格的颜色
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # 数据存储
        self.data_file = "todos.json"
        self.todos: List[TodoItem] = []
        self.todo_widgets: List[Dict] = []

        # 初始化 UI
        self.setup_ui()

        # 加载数据
        self.load_todos()

    def setup_ui(self):
        """设置用户界面"""

        # 主容器
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # 标题区域
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="我的待办事项",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#1a73e8"
        )
        self.title_label.pack(side="left")

        # 统计信息
        self.stats_label = ctk.CTkLabel(
            self.header_frame,
            text="0 个任务",
            font=ctk.CTkFont(size=14),
            text_color="#5f6368"
        )
        self.stats_label.pack(side="right")

        # 输入区域
        self.input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.input_frame.pack(fill="x", pady=(0, 20))

        self.todo_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="添加新的待办事项...",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2,
            corner_radius=10
        )
        self.todo_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.todo_entry.bind("<Return>", lambda e: self.add_todo())

        self.add_button = ctk.CTkButton(
            self.input_frame,
            text="添加",
            command=self.add_todo,
            height=45,
            width=100,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        self.add_button.pack(side="right")

        # 待办事项列表容器（带滚动）
        self.list_container = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color="transparent",
            corner_radius=0
        )
        self.list_container.pack(fill="both", expand=True)

        # 底部操作栏
        self.bottom_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.bottom_frame.pack(fill="x", pady=(20, 0))

        self.clear_completed_button = ctk.CTkButton(
            self.bottom_frame,
            text="清除已完成",
            command=self.clear_completed,
            height=35,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color="#ea4335",
            hover_color="#c5221f"
        )
        self.clear_completed_button.pack(side="left")

        self.theme_button = ctk.CTkButton(
            self.bottom_frame,
            text="切换主题",
            command=self.toggle_theme,
            height=35,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            fg_color="#5f6368",
            hover_color="#3c4043"
        )
        self.theme_button.pack(side="right")

    def add_todo(self):
        """添加新的待办事项"""
        text = self.todo_entry.get().strip()
        if not text:
            return

        # 创建新的待办事项
        todo = TodoItem(text)
        self.todos.append(todo)

        # 清空输入框
        self.todo_entry.delete(0, "end")

        # 更新界面
        self.render_todo(todo, len(self.todos) - 1)
        self.update_stats()

        # 保存数据
        self.save_todos()

    def render_todo(self, todo: TodoItem, index: int):
        """渲染单个待办事项"""

        # 待办事项容器
        todo_frame = ctk.CTkFrame(
            self.list_container,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#e8eaed"
        )
        todo_frame.pack(fill="x", pady=5, padx=2)

        # 复选框
        checkbox = ctk.CTkCheckBox(
            todo_frame,
            text="",
            command=lambda: self.toggle_todo(index),
            width=20,
            checkbox_width=20,
            checkbox_height=20,
            corner_radius=5,
            fg_color="#1a73e8",
            hover_color="#1557b0"
        )
        checkbox.pack(side="left", padx=(15, 10), pady=15)
        if todo.completed:
            checkbox.select()

        # 文本标签
        text_color = "#5f6368" if todo.completed else "#202124"
        font_overstrike = todo.completed

        text_label = ctk.CTkLabel(
            todo_frame,
            text=todo.text,
            font=ctk.CTkFont(size=14, overstrike=font_overstrike),
            text_color=text_color,
            anchor="w"
        )
        text_label.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=15)

        # 删除按钮
        delete_button = ctk.CTkButton(
            todo_frame,
            text="✕",
            command=lambda: self.delete_todo(index),
            width=30,
            height=30,
            font=ctk.CTkFont(size=16),
            corner_radius=5,
            fg_color="transparent",
            text_color="#5f6368",
            hover_color="#f1f3f4"
        )
        delete_button.pack(side="right", padx=10, pady=15)

        # 保存组件引用
        widget_dict = {
            "frame": todo_frame,
            "checkbox": checkbox,
            "label": text_label,
            "delete_button": delete_button
        }

        if index >= len(self.todo_widgets):
            self.todo_widgets.append(widget_dict)
        else:
            self.todo_widgets[index] = widget_dict

    def toggle_todo(self, index: int):
        """切换待办事项的完成状态"""
        if index < len(self.todos):
            self.todos[index].completed = not self.todos[index].completed
            self.refresh_todos()
            self.save_todos()

    def delete_todo(self, index: int):
        """删除待办事项"""
        if index < len(self.todos):
            del self.todos[index]
            self.refresh_todos()
            self.save_todos()

    def clear_completed(self):
        """清除所有已完成的待办事项"""
        self.todos = [todo for todo in self.todos if not todo.completed]
        self.refresh_todos()
        self.save_todos()

    def refresh_todos(self):
        """刷新待办事项列表显示"""
        # 清除现有的组件
        for widget_dict in self.todo_widgets:
            widget_dict["frame"].destroy()
        self.todo_widgets.clear()

        # 排序：未完成事项置顶，已完成事项在底部
        self.todos.sort(key=lambda todo: todo.completed)

        # 重新渲染所有待办事项
        for index, todo in enumerate(self.todos):
            self.render_todo(todo, index)

        self.update_stats()

    def update_stats(self):
        """更新统计信息"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo.completed)
        self.stats_label.configure(text=f"{total} 个任务 ({completed} 已完成)")

    def toggle_theme(self):
        """切换主题（浅色/深色）"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "Light" else "light"
        ctk.set_appearance_mode(new_mode)

    def save_todos(self):
        """保存待办事项到文件"""
        data = [todo.to_dict() for todo in self.todos]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_todos(self):
        """从文件加载待办事项"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.todos = [TodoItem.from_dict(item) for item in data]
                    self.refresh_todos()
            except Exception as e:
                print(f"加载数据失败: {e}")


def main():
    """主函数"""
    app = TodoListApp()
    app.mainloop()


if __name__ == "__main__":
    main()
