CREATE TABLE messages (
	message_id SERIAL PRIMARY KEY,
	message_content TEXT NOT NULL CONSTRAINT content_constraint CHECK(message_content != ''),
	from_client BOOL DEFAULT True,
	sending_datetime TIMESTAMP DEFAULT NOW(),
	handling_model_type VARCHAR(13) NOT NULL DEFAULT 'text', -- [online voice, offline voice, text]
	response_for_message_id INTEGER DEFAULT -1  -- (-1) means that message is requesting
);

-- <#>------------------------<#> Testing content <#>------------------------<#> --

INSERT INTO messages (message_content, from_client, response_for_message_id) VALUES
	('Привет!', true, -1),
	('Привет, я Гарик, чем могу помочь?', false, 1),
	('Когда уже релиз? :)', true, -1),
	('Скоро', false, 3);

-- <#>------------------------<#> Testing content <#>------------------------<#> --

SELECT * FROM messages;
