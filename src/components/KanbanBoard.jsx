import { useEffect, useState } from "react"
import {
    createTask,
    deleteTask,
    getTasks,
    updateTaskStatus
} from "../api"
import "./Kanban_board.css"

function Kanban_board({ accessToken }) {

    const [columns, setColumns] = useState({
        todo: {
            name: "To Do",
            items: []
        },
        inProgress: {
            name: "In Progress",
            items: []
        },
        done: {
            name: "Done",
            items: []
        }
    })

    const [newTaskName, setNewTaskName] = useState("")
    const [newTaskDescription, setNewTaskDescription] = useState("")

    const [activeColumn, setActiveColumn] = useState(null)

    const [draggedItem, setDraggedItem] = useState(null)

    const [loading, setLoading] = useState(true)

    const [error, setError] = useState("")


    useEffect(() => {

        loadTasks()

    }, [accessToken])


    const loadTasks = async () => {

        if (!accessToken) {
            return
        }

        setLoading(true)

        const result = await getTasks(accessToken)

        if (result.status !== 200) {
            setError(
                result.data?.message ||
                "Failed to load tasks"
            )

            setLoading(false)

            return
        }

        const tasks = Array.isArray(result.data)
            ? result.data
            : result.data?.tasks || []

        const newColumns = {
            todo: {
                name: "To Do",
                items: []
            },
            inProgress: {
                name: "In Progress",
                items: []
            },
            done: {
                name: "Done",
                items: []
            }
        }

        tasks.forEach((task) => {

            if (newColumns[task.status]) {

                newColumns[task.status].items.push(task)

            }

        })

        setColumns(newColumns)

        setLoading(false)
    }


    const openCreateTask = (columnId) => {

        setActiveColumn(columnId)

        setNewTaskName("")
        setNewTaskDescription("")

    }


    const closeCreateTask = () => {

        setActiveColumn(null)

        setNewTaskName("")
        setNewTaskDescription("")

    }


    const addNewTask = async () => {

        if (!newTaskName.trim()) {
            return
        }

        const status = activeColumn

        const result = await createTask(
            accessToken,
            newTaskName,
            newTaskDescription,
            status
        )

        if (result.status !== 200 && result.status !== 201) {

            setError(
                result.data?.message ||
                "Failed to create task"
            )

            return
        }

        const task = result.data?.task || result.data

        setColumns((currentColumns) => ({
            ...currentColumns,
            [status]: {
                ...currentColumns[status],
                items: [
                    ...currentColumns[status].items,
                    task
                ]
            }
        }))

        closeCreateTask()
    }


    const removeTask = async (columnId, taskId) => {

        const previousColumns = columns

        setColumns((currentColumns) => ({
            ...currentColumns,
            [columnId]: {
                ...currentColumns[columnId],
                items: currentColumns[columnId].items.filter(
                    (item) => item.id !== taskId
                )
            }
        }))

        const result = await deleteTask(
            accessToken,
            taskId
        )

        if (result.status !== 200) {

            console.error(
                "Failed to delete task:",
                result.data
            )

            setColumns(previousColumns)

        }
    }


    const handleDragStart = (columnId, item) => {

        setDraggedItem({
            columnId,
            item
        })
    }


    const handleDragOver = (e) => {

        e.preventDefault()

    }


    const handleDrop = (e, targetColumnId) => {

        e.preventDefault()

        if (!draggedItem) {
            return
        }

        const {
            columnId: sourceColumnId,
            item
        } = draggedItem

        if (sourceColumnId === targetColumnId) {

            setDraggedItem(null)

            return
        }

        const updatedColumns = {
            ...columns,

            [sourceColumnId]: {
                ...columns[sourceColumnId],

                items: columns[sourceColumnId].items.filter(
                    (i) => i.id !== item.id
                )
            },

            [targetColumnId]: {
                ...columns[targetColumnId],

                items: [
                    ...columns[targetColumnId].items,
                    {
                        ...item,
                        status: targetColumnId
                    }
                ]
            }
        }

        /*
         * Update the UI immediately.
         */
        setColumns(updatedColumns)

        setDraggedItem(null)

        /*
         * Save the new status in the background.
         */
        updateTaskStatus(
            accessToken,
            item.id,
            targetColumnId
        )
        .then((result) => {

            if (result.status !== 200) {

                console.error(
                    "Failed to update task status:",
                    result.data
                )

            }

        })
        .catch((error) => {

            console.error(
                "Failed to update task status:",
                error
            )

        })
    }


    const formatDuration = (seconds) => {

        if (seconds === null || seconds === undefined) {
            return null
        }

        if (seconds < 0) {
            seconds = 0
        }

        const totalSeconds = Math.floor(seconds)

        const hours = Math.floor(
            totalSeconds / 3600
        )

        const minutes = Math.floor(
            (totalSeconds % 3600) / 60
        )

        const remainingSeconds =
            totalSeconds % 60

        if (hours > 0) {

            return `${hours}h ${minutes}m`

        }

        if (minutes > 0) {

            return `${minutes}m ${remainingSeconds}s`

        }

        return `${remainingSeconds}s`
    }


    const getTaskDuration = (task) => {

        if (!task.started_at) {
            return null
        }

        const start =
            new Date(task.started_at).getTime()

        let end

        if (task.completed_at) {

            end =
                new Date(task.completed_at).getTime()

        } else {

            end = Date.now()

        }

        const seconds =
            (end - start) / 1000

        return formatDuration(seconds)
    }


    if (loading) {

        return (
            <div className="kanban-board">
                <p>Loading tasks...</p>
            </div>
        )
    }


    return (
        <>
            <div className="kanban-board">

                <div className="kanban-columns">

                    {Object.keys(columns).map((columnId) => {

                        const column =
                            columns[columnId]

                        return (
                            <div
                                key={columnId}
                                className="task-column"
                                onDragOver={handleDragOver}
                                onDrop={(e) =>
                                    handleDrop(
                                        e,
                                        columnId
                                    )
                                }
                            >

                                <div className="column-header">

                                    <div className="column-title">

                                        {column.name}

                                        <span className="column-count">
                                            {column.items.length}
                                        </span>

                                    </div>

                                    <button
                                        type="button"
                                        className="add-task-button"
                                        onClick={() =>
                                            openCreateTask(
                                                columnId
                                            )
                                        }
                                    >
                                        +
                                    </button>

                                </div>


                                <div className="column-tasks">

                                    {column.items.length === 0 ? (

                                        <div className="empty-column">
                                            Drop tasks here
                                        </div>

                                    ) : (

                                        column.items.map((item) => {

                                            const duration =
                                                getTaskDuration(
                                                    item
                                                )

                                            return (
                                                <div
                                                    key={item.id}
                                                    className="task"
                                                    draggable
                                                    onDragStart={() =>
                                                        handleDragStart(
                                                            columnId,
                                                            item
                                                        )
                                                    }
                                                >

                                                    <div className="task-content">

                                                        <div className="task-name">
                                                            {item.name}
                                                        </div>

                                                        {item.description && (
                                                            <div className="task-description">
                                                                {item.description}
                                                            </div>
                                                        )}

                                                        {duration && (
                                                            <div className="task-time">
                                                                Time: {duration}
                                                            </div>
                                                        )}

                                                    </div>


                                                    <button
                                                        type="button"
                                                        className="delete-button"
                                                        onClick={() =>
                                                            removeTask(
                                                                columnId,
                                                                item.id
                                                            )
                                                        }
                                                    >
                                                        x
                                                    </button>

                                                </div>
                                            )

                                        })

                                    )}

                                </div>

                            </div>
                        )

                    })}

                </div>

            </div>


            {error && (
                <p className="error">
                    {error}
                </p>
            )}


            {activeColumn && (

                <div
                    className="modal-overlay"
                    onClick={closeCreateTask}
                >

                    <div
                        className="create-task-modal"
                        onClick={(e) =>
                            e.stopPropagation()
                        }
                    >

                        <div className="modal-header">

                            <div>

                                <h2>
                                    Add Task
                                </h2>

                                <span>
                                    {columns[activeColumn].name}
                                </span>

                            </div>

                            <button
                                type="button"
                                className="modal-close-button"
                                onClick={closeCreateTask}
                            >
                                x
                            </button>

                        </div>


                        <div className="modal-body">

                            <label>
                                Task name
                            </label>

                            <input
                                type="text"
                                value={newTaskName}
                                onChange={(e) =>
                                    setNewTaskName(
                                        e.target.value
                                    )
                                }
                                placeholder="Enter task name"
                                autoFocus
                            />


                            <label>
                                Description
                            </label>

                            <textarea
                                value={newTaskDescription}
                                onChange={(e) =>
                                    setNewTaskDescription(
                                        e.target.value
                                    )
                                }
                                placeholder="Enter task description"
                            />

                        </div>


                        <div className="modal-footer">

                            <button
                                type="button"
                                className="cancel-button"
                                onClick={closeCreateTask}
                            >
                                Cancel
                            </button>

                            <button
                                type="button"
                                className="create-button"
                                onClick={addNewTask}
                            >
                                Create
                            </button>

                        </div>

                    </div>

                </div>

            )}

        </>
    )
}

export default Kanban_board