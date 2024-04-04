CREATE TABLE messages (
	message_id SERIAL PRIMARY KEY,
	message_content TEXT NOT NULL CONSTRAINT content_constraint CHECK(message_content != ''),
	from_client BOOL DEFAULT True,
	sending_datetime DATE DEFAULT NOW(),
	handling_model_type VARCHAR(13) NOT NULL DEFAULT 'text', -- [online voice, offline voice, text]
	response_for_message_id INTEGER DEFAULT -1 -- (-1) means that message is requesting
)

SELECT * FROM messages;
