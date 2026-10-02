import { useState } from "react";
import { createTrelloCard } from "../services/api/trello";

function Trello() {
    const [name, setName] = useState("");
    const [desc, setDesc] = useState("");
    const [message, setMessage] = useState("");

    async function handleCreateCard(e) {
        e.preventDefault();

        setMessage("Creating card...");

        try {
            const result = await createTrelloCard(
                name,
                desc
            );

            if (result.status === 201) {
                setMessage("Card created successfully");

                setName("");
                setDesc("");

                return;
            }

            setMessage(
                result.data.msg || "Failed to create card"
            );

        } catch (error) {
            console.error(error);
            setMessage("Request failed");
        }
    }

    return (
        <div className="trello-page">

            <div className="trello-card">

                <h1>Create Trello Card</h1>

                <form onSubmit={handleCreateCard}>

                    <div className="form-group">

                        <label>
                            Card Name
                        </label>

                        <input
                            type="text"
                            value={name}
                            onChange={(e) =>
                                setName(e.target.value)
                            }
                            placeholder="Enter card name"
                        />

                    </div>


                    <div className="form-group">

                        <label>
                            Description
                        </label>

                        <textarea
                            value={desc}
                            onChange={(e) =>
                                setDesc(e.target.value)
                            }
                            placeholder="Enter card description"
                            rows="6"
                        />

                    </div>


                    <button type="submit">
                        Create Card
                    </button>

                </form>


                {message && (
                    <div className="trello-status">
                        {message}
                    </div>
                )}

            </div>

        </div>
    );
}

export default Trello;